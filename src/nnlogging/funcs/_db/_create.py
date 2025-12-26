from collections.abc import Sequence
from pathlib import Path
from uuid import UUID

import duckdb

from nnlogging.exceptions import (
    RunDuplicatePrimaryKeyError,
    RunNotUniqueError,
    RunNullColError,
)
from nnlogging.typings import DuckConnection, ExperimentRun


__all__ = ["create_run", "create_tables"]


def _sqlstr_create_tables() -> str:
    with Path(__file__).parent.joinpath("create_tables.sql").open("r") as f:
        return f.read()


def create_tables(con: DuckConnection) -> None:
    _ = con.execute(_sqlstr_create_tables())


def _sqlstr_create_run() -> str:
    with Path(__file__).parent.joinpath("create_run.sql").open("r") as f:
        return f.read()


def create_run(
    con: DuckConnection,
    uuid: UUID,
    exprun: ExperimentRun,
    parents: Sequence[UUID] | None = None,  # MAYBE: validate parents
) -> None:
    grp = exprun.grp
    exp = exprun.exp
    run = exprun.run
    try:
        _ = con.execute(_sqlstr_create_run(), (uuid, grp, exp, run, parents))
    except duckdb.ConstraintException as e:
        emsg = str(e)
        if "violates unique constraint" in emsg:
            raise RunNotUniqueError(exprun) from e
        if "violates primary key constraint" in emsg:
            raise RunDuplicatePrimaryKeyError(uuid) from e
        for col in ("uuid", "exp"):
            if f"experiments.{col}" in emsg:
                raise RunNullColError(col) from e
        raise  # pragma: no cover
