import sys
from collections.abc import Mapping
from datetime import datetime
from types import TracebackType
from typing import Callable, Literal, TypeAlias, TypedDict

from rich.console import Console as RichConsole
from rich.logging import RichHandler
from rich.progress import Progress as RichProgress, TaskID as RichTaskID
from rich.style import Style as RichStyle
from rich.text import Text as RichText

from nnlogging.typings.generics import Pathlike
from nnlogging.typings.protocols import TerminalWritable, Writable

if sys.version_info >= (3, 11):
    from typing import NotRequired, Required
else:
    from typing_extensions import NotRequired, Required


Sink: TypeAlias = Writable | TerminalWritable
GenericPath = Pathlike[str] | Pathlike[bytes]
FormatTimeCallable: TypeAlias = Callable[[datetime], RichText]


class Branch(TypedDict):
    console: Required[RichConsole]
    handler: Required[RichHandler]
    tasks: Required[dict[str, RichTaskID]]
    progress: Required[RichProgress | None]


JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


class ConsolePrintOptions(TypedDict):
    sep: NotRequired[str]
    end: NotRequired[str]
    style: NotRequired[str | RichStyle | None]
    justify: NotRequired[JustifyMethod | None]
    overflow: NotRequired[OverflowMethod | None]
    no_wrap: NotRequired[bool | None]
    emoji: NotRequired[bool | None]
    markup: NotRequired[bool | None]
    highlight: NotRequired[bool | None]
    width: NotRequired[int | None]
    height: NotRequired[int | None]
    crop: NotRequired[bool]
    soft_wrap: NotRequired[bool | None]
    new_line_start: NotRequired[bool]


_SysExcInfo: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None]
    | tuple[None, None, None]
)
ExcInfo: TypeAlias = None | bool | _SysExcInfo | BaseException


class LogOptions(TypedDict):
    exc_info: NotRequired[ExcInfo]
    stack_info: NotRequired[bool]
    stacklevel: NotRequired[int]
    extra: NotRequired[Mapping[str, object] | None]
