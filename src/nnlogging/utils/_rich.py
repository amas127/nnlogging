from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from nnlogging.helpers import asdict
from nnlogging.typings import (
    LogMsgFormatter,
    RichConsole,
    RichHandler,
    RichProgress,
    RichTaskID,
    Sink,
)


if TYPE_CHECKING:
    from nnlogging.options import (
        ConsoleFullOpt,
        HandlerFullOpt,
        ProgressFullOpt,
        TaskFullOpt,
    )


__all__ = ["get_rconsole", "get_rhandler", "get_rprogress", "get_rtask"]


def get_rconsole(sink: Sink, kwargs: ConsoleFullOpt) -> RichConsole:
    if isinstance(sink, str):
        sink = getattr(sys, sink)
    return RichConsole(file=sink, **asdict(kwargs))  # pyright: ignore[reportArgumentType]


def get_rhandler(console: RichConsole, kwargs: HandlerFullOpt) -> RichHandler:
    hdlr = RichHandler(console=console, **asdict(kwargs.setup))
    hdlr.setFormatter(LogMsgFormatter(f) if isinstance(f := kwargs.msgfmt, str) else f)
    return hdlr


def get_rprogress(console: RichConsole, kwargs: ProgressFullOpt) -> RichProgress:
    return RichProgress(*kwargs.columns, console=console, **asdict(kwargs.setup))  # pyright: ignore[reportOptionalIterable]


def get_rtask(progress: RichProgress, kwargs: TaskFullOpt) -> RichTaskID:
    return progress.add_task(**asdict(kwargs))
