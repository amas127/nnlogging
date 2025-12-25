from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TypedDict
from uuid import UUID

from nnlogging.typings import Required


__all__ = ["RunFullOpt", "RunParOpt"]


@dataclass(kw_only=True)
class RunFullOpt:
    storage_dir: str = field(default=".nnlogging")
    tables_file: str = field(default="tables.db")
    artifacts_dir: str = field(default="artifacts")
    uuid: UUID = field()
    group: str = field(default="")
    experiment: str = field()
    run: str = field(default="")
    parents: Sequence[UUID] | None = field(default=None)


class RunParOpt(TypedDict, total=False):
    storage_dir: str
    tables_file: str
    artifacts_dir: str
    uuid: Required[UUID]
    group: str
    experiment: Required[str]
    run: str
    parents: Sequence[UUID] | None
