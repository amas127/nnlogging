from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.typings import (
    Level,
    LogMsgFormatter,
    LogTimeFormatter,
    RichHighlighter,
    RichNullHighlighter,
)


__all__ = ["HandlerFullOpt", "HandlerParOpt", "HandlerSetupFullOpt"]


@dataclass(kw_only=True)
class HandlerSetupFullOpt:
    level: Level = field(default="DEBUG")
    show_level: bool = field(default=True)
    show_time: bool = field(default=True)
    show_path: bool = field(default=True)
    log_time_format: str | LogTimeFormatter = field(default="[%x %X]")
    omit_repeated_times: bool = field(default=True)
    markup: bool = field(default=True)
    highlighter: RichHighlighter = field(default_factory=RichNullHighlighter)
    rich_tracebacks: bool = field(default=True)
    tracebacks_width: int | None = field(default=None)
    tracebacks_code_width: int = field(default=88)
    tracebacks_extra_lines: int = field(default=0)
    tracebacks_max_frames: int = field(default=1)
    tracebacks_show_locals: bool = field(default=False)
    locals_max_length: int = field(default=10)
    locals_max_string: int = field(default=88)


@dataclass(kw_only=True)
class HandlerFullOpt:
    setup: HandlerSetupFullOpt = field(default_factory=HandlerSetupFullOpt)
    msgfmt: str | LogMsgFormatter | None = field(default=None)

    def __post_init__(self) -> None:
        self.msgfmt = self.msgfmt or "%(message)s"


class HandlerParOpt(TypedDict, total=False):
    level: Level
    show_level: bool
    show_time: bool
    show_path: bool
    log_time_format: str | LogTimeFormatter
    log_message_format: str | LogMsgFormatter | None
    omit_repeated_times: bool
    markup: bool
    highlighter: RichHighlighter
    rich_tracebacks: bool
    tracebacks_width: int | None
    tracebacks_code_width: int
    tracebacks_extra_lines: int
    tracebacks_max_frames: int
    tracebacks_show_locals: bool
    locals_max_length: int
    locals_max_string: int
