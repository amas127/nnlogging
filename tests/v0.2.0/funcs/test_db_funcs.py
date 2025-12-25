import math
from uuid import uuid4

import duckdb
import pytest

from nnlogging.exceptions import (
    RunDuplicatePrimaryKeyError,
    RunNotFoundError,
    RunNotUniqueError,
    RunNullColError,
    RunUpdateArchivedError,
    TrackStepOutRangeError,
)
from nnlogging.funcs import (
    add_extras,
    add_hparams,
    add_summaries,
    add_tags,
    archive_run,
    close_run,
    create_run,
    create_tables,
    remove_tags,
    track,
    update_status,
)
from nnlogging.helpers import loads
from nnlogging.typings import ExperimentRun, StepTrack
from nnlogging.utils import check_exprun_updatable


@pytest.fixture
def con():
    return duckdb.connect()


@pytest.fixture
def con_table():
    con = duckdb.connect()
    create_tables(con)
    return con


@pytest.fixture
def random_exp(random_text):
    return random_text(8)


@pytest.fixture
def random_uuid():
    return uuid4()


@pytest.fixture
def random_met():
    return {
        "int": 456456,
        "float": 4.2,
        "str": "some str here",
        "nested": {
            "int": 456456,
            "float": 4.2,
            "str": "some str here",
            "nested": {"nested": "hi"},
            "seq": ["ch1", "ch2"],
        },
        "seq": ["ch1", "ch2"],
    }


@pytest.fixture
def random_step(random_int):
    return random_int(10)


class TestDBCreate:
    def test_create_tables(self, con):
        create_tables(con)
        assert con.execute("DESCRIBE experiments").fetchall()
        assert con.execute("DESCRIBE rawtracks").fetchall()

    def test_create_run_default(self, con_table, random_exp, random_uuid):
        create_run(con_table, random_uuid, exprun=ExperimentRun(random_exp))
        experiments = con_table.execute("SELECT uuid, exp FROM experiments").fetchall()
        assert len(experiments) == 1
        assert experiments[0] == (random_uuid, random_exp)

    def test_create_run_nulluuid(self, con_table, random_exp):
        with pytest.raises(RunNullColError, match="'uuid' is NULL"):
            create_run(con_table, None, exprun=ExperimentRun(exp=random_exp))

    def test_create_run_nullexp(self, con_table, random_uuid):
        with pytest.raises(RunNullColError, match="'exp' is NULL"):
            create_run(con_table, random_uuid, exprun=ExperimentRun(exp=None))

    def test_create_run_duplicate_exprun(self, con_table, random_uuid, random_exp):
        create_run(con_table, random_uuid, exprun=ExperimentRun(exp=random_exp))
        with pytest.raises(RunNotUniqueError, match=f"(grp=, exp={random_exp}, run=)"):
            create_run(con_table, random_uuid, exprun=ExperimentRun(exp=random_exp))

    def test_create_run_duplicate_uuid(self, con_table, random_uuid):
        create_run(con_table, random_uuid, exprun=ExperimentRun(exp="exp1"))
        with pytest.raises(RunDuplicatePrimaryKeyError, match=f"'{random_uuid.hex}'"):
            create_run(con_table, random_uuid, exprun=ExperimentRun(exp="exp2"))

    @pytest.mark.parametrize("grp", ["", "somegrp"])
    @pytest.mark.parametrize("run", ["", "somerun"])
    def test_create_run_group_and_run(
        self, grp, run, con_table, random_exp, random_uuid
    ):
        exprun = ExperimentRun(grp=grp, exp=random_exp, run=run)
        create_run(con_table, random_uuid, exprun=exprun)
        table = con_table.execute("SELECT grp, run FROM experiments").fetchall()
        assert table[0] == (grp, run)

    @pytest.mark.parametrize("parents", [None, [], [uuid4(), uuid4()]])
    def test_create_run_parents(self, parents, con_table, random_exp, random_uuid):
        exprun = ExperimentRun(exp=random_exp)
        create_run(con_table, random_uuid, exprun=exprun, parents=parents)
        table = con_table.execute("SELECT parents FROM experiments").fetchall()
        assert table[0] == (parents,)


@pytest.fixture
def open_run(con_table, random_uuid, random_exp):
    exprun = ExperimentRun(exp=random_exp)
    create_run(con_table, random_uuid, exprun)
    return random_uuid, exprun


@pytest.fixture
def closed_run(con_table, open_run):
    uuid, exprun = open_run
    close_run(con_table, uuid)
    return uuid, exprun


@pytest.fixture
def archived_run(con_table, open_run):
    uuid, exprun = open_run
    archive_run(con_table, uuid)
    return uuid, exprun


@pytest.fixture
def random_steptrack(random_met):
    return StepTrack(
        met=random_met,
        atf=[{"path": "fake-path", "storage": "fake-storage"}],
        ctx={},
    )


class TestTrack:
    def test_track_default(self, con_table, open_run, random_steptrack):
        uuid, _ = open_run
        step = 1
        track(con_table, uuid, step=step, item=random_steptrack)
        row = con_table.execute(
            "SELECT step, met, atf, ctx FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()
        assert loads(row) == (
            step,
            random_steptrack.met,
            random_steptrack.atf,
            random_steptrack.ctx,
        )

    def test_track_multiple_steps(self, con_table, open_run):
        uuid, _ = open_run
        for step in [1, 2, 3]:
            track(con_table, uuid, step=step, item=StepTrack(met={"step": step}))
        rows = con_table.execute(
            "SELECT step FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchall()
        assert rows == [(1,), (2,), (3,)]

    def test_track_invalid_step(self, con_table, open_run):
        step = -1
        uuid, _ = open_run
        with pytest.raises(TrackStepOutRangeError):
            track(con_table, uuid, step=step, item=StepTrack(met={}))

    def test_track_conversion_error(self, con_table, open_run):
        uuid, _ = open_run
        # Passing a string that is not a UUID to trigger ConversionException in DuckDB
        # although the type hint says UUID, at runtime we can pass anything.
        with pytest.raises(duckdb.ConversionException):
            track(con_table, "not-a-uuid", step=1, item=StepTrack(met={}))

    def test_track_none_values(self, con_table, open_run):
        uuid, _ = open_run
        track(con_table, uuid, step=1, item=StepTrack(met=None, atf=None, ctx=None))
        row = con_table.execute(
            "SELECT met, atf, ctx FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()
        assert row == (None, None, None)

    @pytest.mark.parametrize(
        "met_present,atf_present,ctx_present",
        [
            (True, True, True),
            (True, True, False),
            (True, False, True),
            (True, False, False),
            (False, True, True),
            (False, True, False),
            (False, False, True),
            (False, False, False),
        ],
    )
    def test_track_all_combinations(
        self, con_table, open_run, random_met, met_present, atf_present, ctx_present
    ):
        uuid, _ = open_run
        step = 1

        # Create StepTrack with appropriate presence/absence of fields
        met = random_met if met_present else None
        atf = (
            [{"path": "test-path", "storage": "test-storage"}] if atf_present else None
        )
        ctx = {"context_key": "context_value"} if ctx_present else None

        item = StepTrack(met=met, atf=atf, ctx=ctx)
        track(con_table, uuid, step=step, item=item)

        # Retrieve and verify
        row = con_table.execute(
            "SELECT step, met, atf, ctx FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()

        assert loads(row) == (step, met, atf, ctx)

    @pytest.mark.parametrize(
        "json_value",
        [
            {},
            [],
            "test",
            42,
            math.pi,
            {"a": {"b": 1}},
            [1, [2, 3]],
        ],
    )
    def test_track_jsonlike_types(self, con_table, open_run, json_value):
        uuid, _ = open_run
        step = 1

        # Test with met
        item = StepTrack(met=json_value, atf=None, ctx=None)
        track(con_table, uuid, step=step, item=item)
        row = con_table.execute(
            "SELECT met FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()
        assert loads(row[0]) == json_value

        # Clear the table for next test
        con_table.execute("DELETE FROM rawtracks WHERE uuid=?", (uuid,))

        # Test with ctx
        item = StepTrack(met=None, atf=None, ctx=json_value)
        track(con_table, uuid, step=step, item=item)
        row = con_table.execute(
            "SELECT ctx FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()
        assert loads(row[0]) == json_value

    @pytest.mark.parametrize(
        "artifacts",
        [
            [],
            [{"path": "p1", "storage": "s1"}],
            [{"path": "p1", "storage": "s1"}, {"path": "p2", "storage": "s2"}],
        ],
    )
    def test_track_artifact_variations(self, con_table, open_run, artifacts):
        uuid, _ = open_run
        step = 1

        item = StepTrack(met=None, atf=artifacts, ctx=None)
        track(con_table, uuid, step=step, item=item)
        row = con_table.execute(
            "SELECT atf FROM rawtracks WHERE uuid=?", (uuid,)
        ).fetchone()
        assert loads(row[0]) == artifacts


class TestUpdateStatus:
    def test_update_status_happy_path(self, con_table, open_run):
        uuid, _ = open_run
        update_status(con_table, uuid, "SUCCESSFUL")
        status = con_table.execute(
            "SELECT status FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert status == "SUCCESSFUL"

    def test_update_status_archived(self, con_table, archived_run):
        uuid, _ = archived_run
        with pytest.raises(RunUpdateArchivedError):
            update_status(con_table, uuid, "FAILED")

    def test_update_status_invalid_value(self, con_table, open_run):
        uuid, _ = open_run
        # DuckDB has a CHECK constraint on status
        with pytest.raises(duckdb.ConstraintException):
            update_status(con_table, uuid, "INVALID_STATUS")


class TestArchiveClose:
    def test_archive_run_effect(self, con_table, open_run):
        uuid, _ = open_run
        archive_run(con_table, uuid)
        archived = con_table.execute(
            "SELECT archived FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert archived is True

    def test_close_run_effect(self, con_table, open_run):
        uuid, _ = open_run
        close_run(con_table, uuid)
        ended_at = con_table.execute(
            "SELECT ended_at FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert ended_at is not None


class TestTags:
    def test_add_tags(self, con_table, open_run):
        uuid, _ = open_run
        tags = ["tag1", "tag2"]
        add_tags(con_table, uuid, tags)
        db_tags = con_table.execute(
            "SELECT tags FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert set(db_tags) == set(tags)

    def test_remove_tags(self, con_table, open_run):
        uuid, _ = open_run
        # Pre-add tags
        initial_tags = ["tag1", "tag2", "tag3"]
        add_tags(con_table, uuid, initial_tags)
        # Remove subset
        remove_tags(con_table, uuid, ["tag1", "tag2"])
        db_tags = con_table.execute(
            "SELECT tags FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert set(db_tags) == {"tag3"}

    def test_tags_non_updatable(self, con_table, archived_run):
        uuid, _ = archived_run
        with pytest.raises(RunUpdateArchivedError):
            add_tags(con_table, uuid, ["tag1"])


class TestJson:
    def test_add_hparams_twice(self, con_table, open_run):
        uuid, _ = open_run
        # Test add_hparams (appends to existing)
        hparams1 = {"lr": 0.001, "batch_size": 32}
        add_hparams(con_table, uuid, hparams1)
        db_hparams = con_table.execute(
            "SELECT hparams FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_hparams) == hparams1

        hparams2 = {"lr": 0.002, "epochs": 100}
        add_hparams(con_table, uuid, hparams2)
        db_hparams = con_table.execute(
            "SELECT hparams FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_hparams) == hparams1 | hparams2

    def test_add_summaries_twice(self, con_table, open_run):
        uuid, _ = open_run
        # Test add_summaries (merges)
        summaries1 = {"accuracy": 0.95, "loss": 0.05}
        add_summaries(con_table, uuid, summaries1)
        db_summaries = con_table.execute(
            "SELECT summaries FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_summaries) == summaries1

        # Test update_summaries (overwrites)
        summaries2 = {"accuracy": 0.98, "f1": 0.92}
        add_summaries(con_table, uuid, summaries2)
        db_summaries = con_table.execute(
            "SELECT summaries FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_summaries) == summaries1 | summaries2

    def test_add_extras_twice(self, con_table, open_run):
        uuid, _ = open_run
        # Test add_extras (merges)
        extras1 = {"notes": "initial run", "version": "1.0"}
        add_extras(con_table, uuid, extras1)
        db_extras = con_table.execute(
            "SELECT extras FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_extras) == extras1

        # Test update_extras (overwrites)
        extras2 = {"notes": "updated run", "version": "2.0"}
        add_extras(con_table, uuid, extras2)
        db_extras = con_table.execute(
            "SELECT extras FROM experiments WHERE uuid=?", (uuid,)
        ).fetchone()[0]
        assert loads(db_extras) == extras2

    def test_json_updates_non_updatable(self, con_table, archived_run):
        uuid, _ = archived_run
        with pytest.raises(RunUpdateArchivedError):
            add_hparams(con_table, uuid, {"lr": 0.001})


class TestHelpers:
    def test_check_exprun_updatable_open(self, con_table, open_run):
        uuid, _ = open_run
        from nnlogging.utils._check import check_exprun_updatable

        assert check_exprun_updatable(con_table, uuid) is True

    def test_check_exprun_updatable_closed(self, con_table, closed_run):
        uuid, _ = closed_run
        from nnlogging.utils._check import check_exprun_updatable

        assert (
            check_exprun_updatable(con_table, uuid) is True
        )  # Closed runs are still updatable

    def test_check_exprun_updatable_archived(self, con_table, archived_run):
        uuid, _ = archived_run
        from nnlogging.utils._check import check_exprun_updatable

        with pytest.raises(RunUpdateArchivedError):
            check_exprun_updatable(con_table, uuid)

    def test_run_not_found_error(self, con_table):
        random_uuid = uuid4()
        with pytest.raises(RunNotFoundError):
            add_tags(con_table, random_uuid, ["tag1"])
        with pytest.raises(RunNotFoundError):
            update_status(con_table, random_uuid, "SUCCESSFUL")
        with pytest.raises(RunNotFoundError):
            track(con_table, random_uuid, step=1, item=StepTrack(met={}))


class TestDBCoverage:
    @pytest.mark.parametrize(
        "func",
        [
            remove_tags,
            add_summaries,
            add_extras,
            archive_run,
            close_run,
        ],
    )
    def test_non_updatable_ops(self, func, con_table, archived_run):
        uuid, _ = archived_run
        with pytest.raises(RunUpdateArchivedError):
            if func in (add_summaries, add_extras):
                func(con_table, uuid, {"key": "val"})
            elif func in (remove_tags,):
                func(con_table, uuid, ["tag"])
            else:
                func(con_table, uuid)

    def test_track_non_updatable(self, con_table, archived_run):
        uuid, _ = archived_run
        with pytest.raises(RunUpdateArchivedError):
            track(con_table, uuid, step=1, item=StepTrack(met={}))

    def test_check_exprun_updatable_no_raise(self, con_table, archived_run):
        uuid, _ = archived_run
        # Test archived run returns False when exc_raise=False
        assert check_exprun_updatable(con_table, uuid, exc_raise=False) is False

        # Test non-existent run returns False when exc_raise=False
        assert check_exprun_updatable(con_table, uuid4(), exc_raise=False) is False

    def test_check_exprun_updatable_callback(self, con_table, archived_run):
        uuid, _ = archived_run
        calls = []

        def callback(msg, *args, **kwargs):
            calls.append(msg % args)

        check_exprun_updatable(con_table, uuid, exc_raise=False, exc_callback=callback)
        assert len(calls) == 1
        assert "cannot be updated" in calls[0]
