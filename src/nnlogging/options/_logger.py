import logging
from dataclasses import dataclass, field
from typing import TypedDict


__all__ = ["LoggerFullOpt", "LoggerParOpt"]


@dataclass(kw_only=True)
class LoggerFullOpt:
    level: int | str = field(default=logging.DEBUG)
    propagate: bool = field(default=True)


class LoggerParOpt(TypedDict, total=False):
    level: int | str
    propagate: bool
