from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime as _datetime
from typing import TYPE_CHECKING, Literal, TypeAlias, TypedDict
from uuid import UUID as _UUID

from duckdb import DuckDBPyConnection as _Connection
from dvc.repo import Repo as _DvcRepo
from numpy.typing import ArrayLike


if TYPE_CHECKING:
    from nnlogging.typings import StrPath


DuckConnection: TypeAlias = _Connection

VJson: TypeAlias = int | float | bool | str | _datetime | _UUID | ArrayLike
Jsonlike: TypeAlias = (
    VJson
    | Sequence["VJson | Jsonlike | None"]
    | Mapping[str, "VJson | Jsonlike | None"]
)


@dataclass
class ExperimentRun:
    exp: str
    grp: str = field(default="")
    run: str = field(default="")


Status: TypeAlias = Literal["RUNNING", "FAILED", "SUCCESSFUL"]


class Artifact(TypedDict):
    path: StrPath
    storage: StrPath


@dataclass
class StepTrack:
    met: Jsonlike | None = field(default=None)
    atf: list[Artifact] | None = field(default=None)
    ctx: Jsonlike | None = field(default=None)

    def __post_init__(self) -> None:
        if self.atf:
            self.atf = [
                {"path": str(a["path"]), "storage": str(a["storage"])} for a in self.atf
            ]


DvcRepo: TypeAlias = _DvcRepo
