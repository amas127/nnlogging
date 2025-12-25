from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from nnlogging.typings import Required


__all__ = ["TaskFullOpt", "TaskParOpt"]


@dataclass(kw_only=True)
class TaskFullOpt:
    total: float | None = field()
    description: str = field(default="")
    completed: float = field(default=0)


class TaskParOpt(TypedDict, total=False):
    total: Required[float | None]
    description: str
    completed: float
