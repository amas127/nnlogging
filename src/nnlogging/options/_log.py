from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.typings import ExcInfoType


__all__ = ["LogFullOpt", "LogParOpt"]


@dataclass(kw_only=True)
class LogFullOpt:
    exc_info: ExcInfoType = field(default=None)
    stack_info: bool = field(default=False)
    stacklevel: int = field(default=1)
    extra: Mapping[str, object] | None = field(default=None)


class LogParOpt(TypedDict, total=False):
    exc_info: ExcInfoType
    stack_info: bool
    stacklevel: int
    extra: Mapping[str, object] | None
