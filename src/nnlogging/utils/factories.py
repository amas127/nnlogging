import logging
from collections.abc import Collection
from dataclasses import asdict
from logging import Formatter as LoggingFormatter
from sys import stderr
from typing import cast

from aim import Run as AimRun
from rich.console import Console as RichConsole
from rich.logging import RichHandler
from rich.progress import Progress as RichProgress, ProgressColumn as RichProgressColumn

from nnlogging.options import (
    BranchConfigOptionDict,
    LoggerConfigOption,
    LoggerConfigOptionDict,
    RichConsoleOption,
    RichConsoleOptionDict,
    RichHandlerOption,
    RichHandlerOptionDict,
    RichProgressOption,
    RichProgressOptionDict,
    RunConfigOption,
    RunConfigOptionDict,
)
from nnlogging.typings.aliases import Branch
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import Sink
from nnlogging.utils.helpers import filter_by_typeddict


def get_rich_console(
    sink: Sink = stderr,
    /,
    **kwargs: Unpack[RichConsoleOptionDict],
):
    options = asdict(RichConsoleOption(**kwargs))
    console = RichConsole(
        file=sink,  # pyright: ignore[reportArgumentType],
        **options,
    )
    return console


def get_rich_handler(
    console: RichConsole | None = None,
    /,
    **kwargs: Unpack[RichHandlerOptionDict],
):
    options = asdict(RichHandlerOption(**kwargs))
    log_message_format = cast(LoggingFormatter, options.pop("log_message_format"))
    handler = RichHandler(
        console=console or get_rich_console(),
        **options,
    )
    handler.setFormatter(log_message_format)
    return handler


def get_rich_progress(
    console: RichConsole | None = None,
    /,
    **kwargs: Unpack[RichProgressOptionDict],
):
    options = asdict(RichProgressOption(**kwargs))
    columns = cast(Collection[str | RichProgressColumn], options.pop("columns"))
    progress = RichProgress(
        *columns,
        console=console,
        **options,
    )
    return progress


def get_logging_logger(
    **kwargs: Unpack[LoggerConfigOptionDict],
):
    options = asdict(LoggerConfigOption(**kwargs))
    logger = logging.getLogger(options["name"])
    logger.setLevel(options["level"])
    logger.propagate = options["propagate"]
    return logger


def get_aim_run(
    **kwargs: Unpack[RunConfigOptionDict],
):
    options = asdict(RunConfigOption(**kwargs))
    run = AimRun(**options)
    return run


def get_branch(
    sink: Sink = stderr,
    /,
    **kwargs: Unpack[BranchConfigOptionDict],
):
    console = get_rich_console(
        sink,
        **filter_by_typeddict(kwargs, RichConsoleOptionDict),
    )
    handler = get_rich_handler(
        console,
        **filter_by_typeddict(kwargs, RichHandlerOptionDict),
    )
    branch = Branch(
        console=console,
        handler=handler,
        progress=None,
        tasks=dict(),
    )
    return branch
