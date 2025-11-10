from collections.abc import Mapping
from types import TracebackType
from typing import TypeAlias, TypedDict

from rich.console import (
    JustifyMethod as RichConsoleJustifyMethod,
    OverflowMethod as RichConsoleOverflowMethod,
)

ExcInfoType: TypeAlias = (
    None
    | bool
    | BaseException
    | tuple[None, None, None]
    | tuple[type[BaseException], BaseException, TracebackType | None]
)


class RichPrintOptionDict(TypedDict, total=False):
    end: str
    justify: RichConsoleJustifyMethod
    no_wrap: bool
    overflow: RichConsoleOverflowMethod
    new_line_start: bool


class LoggingLogOptionDict(TypedDict, total=False):
    exc_info: ExcInfoType
    stack_info: bool
    stacklevel: int
    extra: Mapping[str, object]


class LogOptionDict(LoggingLogOptionDict, RichPrintOptionDict): ...
