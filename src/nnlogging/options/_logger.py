from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.helpers import get_level


__all__ = ["LoggerFullOpt", "LoggerParOpt"]


@dataclass(kw_only=True)
class LoggerFullOpt:
    level: int | str = field(default=get_level("DEBUG"))
    propagate: bool = field(default=True)


class LoggerParOpt(TypedDict, total=False):
    level: int | str
    propagate: bool
