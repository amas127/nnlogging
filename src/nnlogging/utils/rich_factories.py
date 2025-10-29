import logging
from collections.abc import Collection
from logging import Formatter as LoggingFormatter
from sys import stderr
from typing import Literal

from rich.console import Console as RichConsole
from rich.highlighter import (
    Highlighter as RichHighlighter,
    NullHighlighter as RichNullHighlighter,
)
from rich.logging import RichHandler
from rich.progress import Progress as RichProgress, ProgressColumn as RichProgressColumn
from rich.theme import Theme as RichTheme

from nnlogging.typings import FormatTimeCallable, Sink


def get_rich_console(
    sink: Sink | None = None,
    /,
    *,
    width: int | None = None,
    height: int | None = None,
    markup: bool = True,
    emoji: bool = True,
    color_system: Literal["auto", "standard", "truecolor"] | None = "auto",
    theme: RichTheme | None = None,
    highlighter: RichHighlighter | None = None,
    soft_wrap: bool = True,
    force_terminal: bool | None = None,
    force_jupyter: bool | None = None,
    force_interactive: bool | None = None,
):
    console = RichConsole(
        file=sink or stderr,  # pyright: ignore[reportArgumentType]
        width=width,
        height=height,
        markup=markup,
        emoji=emoji,
        color_system=color_system,
        theme=theme,
        highlight=highlighter is not None
        and not isinstance(highlighter, RichNullHighlighter),
        highlighter=highlighter or RichNullHighlighter(),
        soft_wrap=soft_wrap,
        force_terminal=force_terminal,
        force_jupyter=force_jupyter,
        force_interactive=force_interactive,
    )
    return console


def get_rich_handler(
    console: RichConsole | None = None,
    /,
    *,
    level: str | int = logging.NOTSET,
    show_level: bool = True,
    show_time: bool = True,
    show_path: bool = True,
    log_time_format: str | FormatTimeCallable = "[%x %X]",
    omit_repeated_times: bool = True,
    markup: bool = True,
    highlighter: RichHighlighter | None = None,
    rich_tracebacks: bool = True,
    tracebacks_show_locals: bool = False,
    log_message_format: str | LoggingFormatter = "%(message)s",
):
    handler = RichHandler(
        console=console or get_rich_console(),
        level=level,
        show_level=show_level,
        show_time=show_time,
        show_path=show_path,
        log_time_format=log_time_format,
        omit_repeated_times=omit_repeated_times,
        markup=markup,
        highlighter=highlighter or RichNullHighlighter(),
        rich_tracebacks=rich_tracebacks,
        tracebacks_show_locals=tracebacks_show_locals,
    )
    match log_message_format:
        case str():
            handler.setFormatter(LoggingFormatter(log_message_format))
        case LoggingFormatter():
            handler.setFormatter(log_message_format)
    return handler


def get_rich_progress_default_columns(
    *,
    markup: bool = True,
):
    from rich.progress import (
        BarColumn,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeRemainingColumn,
    )

    spinner_column = SpinnerColumn(
        spinner_name="dots",
        style="progress.spinner",
        finished_text=" ",
    )
    text_column = TextColumn(
        text_format="{task.description}",
        style="progress.description",
        justify="left",
        markup=markup,
    )
    bar_column = BarColumn(bar_width=40)
    task_progress_column = TaskProgressColumn(
        text_format="{task.percentage:>3.0f}%",
        text_format_no_percentage="",
        style="progress.percentage",
        justify="right",
        markup=markup,
        show_speed=True,
    )
    time_remaining_column = TimeRemainingColumn(
        compact=False,
        elapsed_when_finished=True,
    )

    return (
        spinner_column,
        text_column,
        bar_column,
        task_progress_column,
        time_remaining_column,
    )


def get_rich_progress(
    console: RichConsole | None = None,
    /,
    *,
    columns: Collection[str | RichProgressColumn] | None = None,
    transient: bool = False,
    refresh_per_second: float = 10,
    speed_estimate_period: float = 3600,
    default_column_markup: bool = True,
):
    progress = RichProgress(
        *(columns or get_rich_progress_default_columns(markup=default_column_markup)),
        console=console,
        transient=transient,
        refresh_per_second=refresh_per_second,
        speed_estimate_period=speed_estimate_period,
    )
    return progress
