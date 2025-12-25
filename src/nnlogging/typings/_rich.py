from __future__ import annotations

from typing import TypeAlias

from rich.console import (
    Console as _Console,
    ConsoleRenderable as _ConsoleRenderable,
    JustifyMethod as _JustifyMethod,
    OverflowMethod as _OverflowMethod,
)
from rich.highlighter import (
    Highlighter as _Highlighter,
    NullHighlighter as _NullHighlighter,
    ReprHighlighter as _ReprHighlighter,
)
from rich.logging import RichHandler as _Handler
from rich.progress import (
    Progress as _Progress,
    ProgressColumn as _ProgressColumn,
    TaskID as _TaskID,
)
from rich.style import Style as _Style
from rich.text import Text as _Text
from rich.theme import Theme as _Theme


RichConsole: TypeAlias = _Console
RichConsoleRenderable: TypeAlias = str | _ConsoleRenderable
RichJustifyMethod: TypeAlias = _JustifyMethod
RichOverflowMethod: TypeAlias = _OverflowMethod

RichHighlighter: TypeAlias = _Highlighter
RichNullHighlighter: TypeAlias = _NullHighlighter
RichReprHighlighter: TypeAlias = _ReprHighlighter

RichHandler: TypeAlias = _Handler

RichProgress: TypeAlias = _Progress
RichProgressColumn: TypeAlias = str | _ProgressColumn
RichTaskID: TypeAlias = _TaskID

RichText: TypeAlias = _Text
RichStyle: TypeAlias = _Style
RichTheme: TypeAlias = _Theme
