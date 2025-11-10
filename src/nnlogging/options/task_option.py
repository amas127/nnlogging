from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.typings.exts import NotRequired, Required


@dataclass(kw_only=True)
class TaskOption:
    description: str = field()
    total: float | None = field()
    completed: float = field(default=0)


class TaskOptionDict(TypedDict):
    description: Required[str]
    total: Required[float | None]
    completed: NotRequired[float]
