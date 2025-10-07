"""nnlog.utils"""

import logging
from collections.abc import Collection
from datetime import datetime
from os import PathLike
from typing import Callable, Literal, TextIO, TypeAlias

from aim import Repo, Run
from rich.console import Console as RichConsole
from rich.highlighter import Highlighter
from rich.progress import ProgressColumn
from rich.text import Text

FormatTimeCallable: TypeAlias = Callable[[datetime], Text]
StrPath: TypeAlias = str | PathLike[str]


__all__ = [
    "get_rich_console",
    "get_rich_handler",
    "get_rich_progress",
    "get_aim_run",
]


def get_rich_console(
    sink: TextIO | None = None,
    width: int | None = None,
    height: int | None = None,
    tab_size: int = 4,
    soft_wrap: bool = True,
    color_system: Literal["auto", "standard", "truecolor"] | None = "auto",
    markup: bool = True,
    highlighter: Highlighter | None = None,
    record: bool = False,
):
    from sys import stderr

    if sink is None:
        sink = stderr

    if highlighter is not None:
        highlight = True
    else:
        from rich.highlighter import NullHighlighter

        highlight = False
        highlighter = NullHighlighter()

    console = RichConsole(
        file=sink,
        width=width,
        height=height,
        tab_size=tab_size,
        soft_wrap=soft_wrap,
        color_system=color_system,
        markup=markup,
        highlight=highlight,
        highlighter=highlighter,
        record=record,
    )

    return console


def get_rich_handler(
    console: RichConsole | None = None,
    name: str | None = None,
    fmt: str | logging.Formatter = "%(message)s",
    level: str | int = logging.INFO,
    show_time: bool = True,
    log_time_format: str | FormatTimeCallable = "[%x %X]",
    omit_repeated_times: bool = True,
    show_level: bool = True,
    show_path: bool = True,
    enable_link_path: bool = True,
    markup: bool = True,
    highlighter: Highlighter | None = None,
    rich_tracebacks: bool = True,
    tracebacks_width: int | None = None,
    tracebacks_code_width: int | None = 88,
    tracebacks_extra_lines: int = 3,
    tracebacks_word_wrap: bool = True,
    tracebacks_max_frames: int = 100,
    tracebacks_show_locals: bool = False,
    locals_max_length: int = 10,
    locals_max_string: int = 80,
):
    from rich.logging import RichHandler

    if console is None:
        console = get_rich_console()

    if isinstance(fmt, str):
        fmt = logging.Formatter(fmt)

    handler = RichHandler(
        console=console,
        level=level,
        show_time=show_time,
        log_time_format=log_time_format,
        omit_repeated_times=omit_repeated_times,
        show_level=show_level,
        show_path=show_path,
        enable_link_path=enable_link_path,
        markup=markup,
        highlighter=highlighter,
        rich_tracebacks=rich_tracebacks,
        tracebacks_width=tracebacks_width,
        tracebacks_code_width=tracebacks_code_width,
        tracebacks_extra_lines=tracebacks_extra_lines,
        tracebacks_word_wrap=tracebacks_word_wrap,
        tracebacks_max_frames=tracebacks_max_frames,
        tracebacks_show_locals=tracebacks_show_locals,
        locals_max_length=locals_max_length,
        locals_max_string=locals_max_string,
    )
    handler.name = name
    handler.setFormatter(fmt=fmt)
    return handler


def get_rich_progress(
    console: RichConsole | None = None,
    columns: Collection[str | ProgressColumn] | None = None,
    expand: bool = False,
    auto_refresh: bool = True,
    refresh_per_second: float = 10,
    speed_estimate_period: float = 3600,
    transient: bool = False,
    redirect_stderr: bool = True,
    redirect_stdout: bool = True,
):
    from rich.progress import Progress

    def get_default_rich_progress_columns():
        from rich.progress import (
            BarColumn,
            SpinnerColumn,
            TaskProgressColumn,
            TextColumn,
            TimeRemainingColumn,
        )

        return (
            SpinnerColumn(
                spinner_name="dots",
                style="progress.spinner",
                finished_text=" ",
            ),
            TextColumn(
                text_format="{task.description}",
                style="progress.description",
                justify="left",
                markup=True,
            ),
            BarColumn(bar_width=40),
            TaskProgressColumn(
                text_format="{task.percentage:>3.0f}%",
                text_format_no_percentage="",
                style="progress.percentage",
                justify="right",
                markup=True,
                show_speed=True,
            ),
            TimeRemainingColumn(
                compact=False,
                elapsed_when_finished=False,
            ),
        )

    if console is None:
        console = get_rich_console()

    if columns is None:
        columns = get_default_rich_progress_columns()

    return Progress(
        *columns,
        console=console,
        auto_refresh=auto_refresh,
        refresh_per_second=refresh_per_second,
        speed_estimate_period=speed_estimate_period,
        transient=transient,
        expand=expand,
        redirect_stderr=redirect_stderr,
        redirect_stdout=redirect_stdout,
    )


def get_aim_run(
    run_hash: str | None = None,
    repo: str | Repo | None = None,
    read_only: bool = False,
    experiment: str | None = None,
    force_resume: bool = False,
    system_tracking_interval: float | None = 10,
    log_system_params: bool = False,
    capture_terminal_logs: bool = False,
):
    return Run(
        run_hash=run_hash,
        repo=repo,
        read_only=read_only,
        experiment=experiment,
        force_resume=force_resume,
        system_tracking_interval=system_tracking_interval,
        log_system_params=log_system_params,
        capture_terminal_logs=capture_terminal_logs,
    )
