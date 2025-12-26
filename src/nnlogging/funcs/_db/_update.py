from pathlib import Path
from uuid import UUID

from nnlogging.typings import DuckConnection, Status
from nnlogging.utils import check_exprun_updatable


__all__ = ["update_status"]


def _sqlstr_update_status() -> str:
    with Path(__file__).parent.joinpath("update_status.sql").open("r") as f:
        return f.read()


def update_status(con: DuckConnection, uuid: UUID, status: Status) -> None:
    if check_exprun_updatable(con, uuid):
        _ = con.execute(_sqlstr_update_status(), (uuid, status))
