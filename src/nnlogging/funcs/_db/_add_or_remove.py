from pathlib import Path
from uuid import UUID

from nnlogging.helpers import dumps
from nnlogging.typings import DuckConnection, Jsonlike
from nnlogging.utils import check_exprun_updatable


__all__ = ["add_extras", "add_hparams", "add_summaries", "add_tags", "remove_tags"]


def _sqlstr_add_tags() -> str:
    with Path(__file__).parent.joinpath("add_tags.sql").open("r") as f:
        return f.read()


def add_tags(
    con: DuckConnection, uuid: UUID, tags: list[str] | tuple[str, ...]
) -> None:
    if check_exprun_updatable(con, uuid):
        _ = con.execute(_sqlstr_add_tags(), (uuid, tags))


def _sqlstr_remove_tags() -> str:
    with Path(__file__).parent.joinpath("remove_tags.sql").open("r") as f:
        return f.read()


def remove_tags(
    con: DuckConnection, uuid: UUID, tags: list[str] | tuple[str, ...]
) -> None:
    if check_exprun_updatable(con, uuid):
        _ = con.execute(_sqlstr_remove_tags(), (uuid, tags))


def _sqlstr_add_hparams() -> str:
    with Path(__file__).parent.joinpath("add_hparams.sql").open("r") as f:
        return f.read()


def add_hparams(con: DuckConnection, uuid: UUID, hparams: Jsonlike) -> None:
    if check_exprun_updatable(con, uuid):
        hparams = dumps(hparams)
        _ = con.execute(_sqlstr_add_hparams(), (uuid, hparams))


def _sqlstr_add_summaries() -> str:
    with Path(__file__).parent.joinpath("add_summaries.sql").open("r") as f:
        return f.read()


def add_summaries(con: DuckConnection, uuid: UUID, summaries: Jsonlike) -> None:
    if check_exprun_updatable(con, uuid):
        summaries = dumps(summaries)
        _ = con.execute(_sqlstr_add_summaries(), (uuid, summaries))


def _sqlstr_add_extras() -> str:
    with Path(__file__).parent.joinpath("add_extras.sql").open("r") as f:
        return f.read()


def add_extras(con: DuckConnection, uuid: UUID, extras: Jsonlike) -> None:
    if check_exprun_updatable(con, uuid):
        extras = dumps(extras)
        _ = con.execute(_sqlstr_add_extras(), (uuid, extras))
