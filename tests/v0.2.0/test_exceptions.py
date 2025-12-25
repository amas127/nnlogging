from uuid import uuid4

import pytest

from nnlogging.exceptions import (
    BranchExistsError,
    BranchNotFoundError,
    LevelNameNotFoundError,
    LevelTypeWeirdError,
    RunDuplicatePrimaryKeyError,
    RunNotFoundError,
    RunNotUniqueError,
    RunNullColError,
    RunUpdateArchivedError,
    StacklevelTypeWeirdError,
    TaskExistsError,
    TaskNotFoundError,
    TrackStepOutRangeError,
)
from nnlogging.typings import ExperimentRun


class TestTaskExistsError:
    def test_empty_branch(self):
        err = TaskExistsError("task")
        exp = "[@Task] 'task' already exists"
        assert str(err) == exp

    def test_nonempty_branch(self):
        err = TaskExistsError("task", ("b", {"tasks": {"t1": 1, "t2": 2}}))
        exp = "[@Task] 'task' already exists in branch 'b' tasks: ('t1', 't2')"
        assert str(err) == exp


class TestBranchExistsError:
    def test_empty_branch(self):
        err = BranchExistsError("br")
        exp = "[@Branch] 'br' already exists"
        assert str(err) == exp

    def test_nonempty_branch(self):
        brs = ["br1", "br2"]
        err = BranchExistsError("br", brs)
        exp = "[@Branch] 'br' already exists in branches: ('br1', 'br2')"
        assert str(err) == exp


class TestTaskNotFoundError:
    def test_empty_branch(self):
        err = TaskNotFoundError("task")
        exp = "[@Task] 'task' not found"
        assert str(err) == exp

    def test_nonempty_branch(self):
        err = TaskNotFoundError(
            "task", [{"tasks": {"t3": 1}}, {"tasks": {"t1": 1, "t2": 2}}]
        )
        exp = "[@Task] 'task' not found in tasks: ('t1', 't2', 't3')"
        assert str(err) == exp


class TestBranchNotFoundError:
    def test_empty_branch(self):
        err = BranchNotFoundError("br")
        exp = "[@Branch] 'br' not found"
        assert str(err) == exp

    def test_nonempty_branch(self):
        err = BranchNotFoundError("br", ["br1", "br2"])
        exp = "[@Branch] 'br' not found in branches: ('br1', 'br2')"
        assert str(err) == exp


@pytest.mark.parametrize(
    "lvl, expected",
    [
        ("debug", "[@Level] 'DEBUG' not found"),
        ("INFO", "[@Level] 'INFO' not found"),
    ],
)
def test_LevelNameNotFoundError(lvl, expected):
    e = LevelNameNotFoundError(lvl)
    assert str(e) == expected


def test_LevelTypeWeirdError():
    e = LevelTypeWeirdError(None)
    assert str(e) == "[@Level] type 'NoneType' is weird"


def test_StacklevelTypeWeirdError():
    e = StacklevelTypeWeirdError("")
    assert str(e) == "[@Stacklevel] type 'str' is weird"


def test_RunNotUniqueError():
    e = RunNotUniqueError(ExperimentRun(exp="1", grp="2", run="3"))
    assert str(e) == "[@Run] run (grp=2, exp=1, run=3) already exists"


def test_RunNotFoundError():
    run = uuid4()
    e = RunNotFoundError(run)
    assert str(e) == f"[@Run] '{run.hex}' not found"


def test_RunDuplicatePrimaryKeyError():
    run = uuid4()
    e = RunDuplicatePrimaryKeyError(run)
    assert str(e) == f"[@Run] '{run.hex}' already exists"


def test_RunNullColError():
    e = RunNullColError("col1")
    assert str(e) == "[@Run] 'col1' is NULL"


def test_RunUpdateArchivedError():
    run = uuid4()
    e = RunUpdateArchivedError(run)
    assert str(e) == f"[@Run] '{run.hex}' is archived"


def test_TrackStepOutRangeError():
    e = TrackStepOutRangeError(-1)
    assert str(e) == "[@Track] step -1 is out of range"
