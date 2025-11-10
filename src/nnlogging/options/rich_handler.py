import logging
from dataclasses import dataclass, field
from logging import Formatter as LoggingFormatter
from typing import TypedDict

from rich.highlighter import (
    Highlighter as RichHighlighter,
    NullHighlighter as RichNullHighlighter,
)

from nnlogging.typings.aliases import FormatTimeCallable


@dataclass(kw_only=True)
class RichHandlerOption:
    level: str | int = field(default=logging.NOTSET)
    show_level: bool = field(default=True)
    show_time: bool = field(default=True)
    show_path: bool = field(default=True)
    log_time_format: str | FormatTimeCallable = field(default="[%x %X]")
    omit_repeated_times: bool = field(default=True)
    markup: bool = field(default=True)
    highlighter: RichHighlighter = field(default_factory=RichNullHighlighter)
    rich_tracebacks: bool = field(default=True)
    tracebacks_extra_lines: int = field(default=0)
    tracebacks_max_frames: int = field(default=1)
    tracebacks_show_locals: bool = field(default=False)
    locals_max_length: int = field(default=10)
    log_message_format: str | LoggingFormatter = field(default="%(message)s")

    def __post_init__(self):
        if isinstance(self.log_message_format, str):
            self.log_message_format = LoggingFormatter(self.log_message_format)


class RichHandlerOptionDict(TypedDict, total=False):
    level: str | int
    show_level: bool
    show_time: bool
    show_path: bool
    log_time_format: str | FormatTimeCallable
    omit_repeated_times: bool
    markup: bool
    highlighter: RichHighlighter
    rich_tracebacks: bool
    tracebacks_show_locals: bool
    log_message_format: str | LoggingFormatter
