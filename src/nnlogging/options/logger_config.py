import logging
from dataclasses import dataclass, field
from typing import TypedDict


@dataclass(kw_only=True)
class LoggerConfigOption:
    name: str = field(default="nnlogging")
    level: int | str = field(default=logging.INFO)
    propagate: bool = field(default=False)


class LoggerConfigOptionDict(TypedDict, total=False):
    name: str
    level: int | str
    propagate: bool
