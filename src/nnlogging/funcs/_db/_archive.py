from pathlib import Path
from uuid import UUID

from nnlogging.typings import DuckConnection
from nnlogging.utils import check_exprun_updatable


__all__ = ["archive_run"]


def _sqlstr_archive_run() -> str:
    with Path(__file__).parent.joinpath("archive_run.sql").open("r") as f:
        return f.read()


def archive_run(con: DuckConnection, uuid: UUID) -> None:
    if check_exprun_updatable(con, uuid):
        _ = con.execute(_sqlstr_archive_run(), (uuid,))
