import sys
import threading
from collections.abc import Collection
from logging import Formatter as LoggingFormatter, Logger as LoggingLogger
from typing import Literal, cast

from aim import Repo as AimRepo, Run as AimRun
from aim.sdk.types import AimObject
from rich.highlighter import Highlighter as RichHighlighter
from rich.progress import ProgressColumn as RichProgressColumn
from rich.theme import Theme as RichTheme

import nnlogging
from nnlogging.typings import (
    Branch,
    ConsolePrintOptions,
    FormatTimeCallable,
    LogOptions,
    Omitable,
    Sink,
)
from nnlogging.utils import (
    BranchConfig,
    LoggerConfig,
    RunConfig,
    add_tag as _add_tag,
    advance as _advance,
    branch_add as _branch_add,
    branch_configure as _branch_configure,
    branch_remove as _branch_remove,
    critical as _critical,
    debug as _debug,
    error as _error,
    exception as _exception,
    info as _info,
    log as _log,
    logger_configure as _logger_configure,
    remove_tag as _remove_tag,
    run_configure as _run_configure,
    task_add as _task_add,
    task_remove as _task_remove,
    track as _track,
    update_metadata as _update_metadata,
    warn as _warn,
)


class Shell:
    def __init__(
        self,
        shell_name: str = "nnlogging",
        /,
        *,
        logger_config: LoggerConfig | None = None,
        run_config: RunConfig | None = None,
        branch_config: BranchConfig | None = None,
    ):
        self.logger: LoggingLogger | None = None
        self.run: AimRun | None = None
        self.branches: dict[str, Branch] = dict()

        self.name: str = shell_name
        self.logger_config: LoggerConfig = logger_config or LoggerConfig()
        self.run_config: RunConfig = run_config or RunConfig()
        self.branch_config: BranchConfig = branch_config or BranchConfig()

    def logger_configure(
        self,
        config: LoggerConfig | None = None,
        /,
        *,
        name: Omitable[str] = ...,
        level: Omitable[int | str] = ...,
        propagate: Omitable[bool] = ...,
    ):
        _logger_configure(
            self,
            config,
            name=name,
            level=level,
            propagate=propagate,
        )

    def run_configure(
        self,
        config: RunConfig | None = None,
        /,
        *,
        experiment: Omitable[str | None] = ...,
        repo: Omitable[str | AimRepo | None] = ...,
        system_tracking_interval: Omitable[float | None] = ...,
        capture_terminal_logs: Omitable[bool] = ...,
        log_system_params: Omitable[bool] = ...,
        run_hash: Omitable[str | None] = ...,
        read_only: Omitable[bool] = ...,
        force_resume: Omitable[bool] = ...,
    ):
        _run_configure(
            self,
            config,
            experiment=experiment,
            repo=repo,
            system_tracking_interval=system_tracking_interval,
            capture_terminal_logs=capture_terminal_logs,
            log_system_params=log_system_params,
            run_hash=run_hash,
            read_only=read_only,
            force_resume=force_resume,
        )

    def branch_configure(
        self,
        config: BranchConfig | None = None,
        /,
        *,
        markup: Omitable[bool] = ...,
        highlighter: Omitable[RichHighlighter] = ...,
        width: Omitable[int | None] = ...,
        height: Omitable[int | None] = ...,
        emoji: Omitable[bool] = ...,
        color_system: Omitable[Literal["auto", "standard", "truecolor"] | None] = ...,
        theme: Omitable[RichTheme] = ...,
        soft_wrap: Omitable[bool] = ...,
        force_terminal: Omitable[bool | None] = ...,
        force_jupyter: Omitable[bool | None] = ...,
        force_interactive: Omitable[bool | None] = ...,
        level: Omitable[str | int] = ...,
        show_level: Omitable[bool] = ...,
        show_time: Omitable[bool] = ...,
        show_path: Omitable[bool] = ...,
        log_time_format: Omitable[str | FormatTimeCallable] = ...,
        omit_repeated_times: Omitable[bool] = ...,
        rich_tracebacks: Omitable[bool] = ...,
        tracebacks_show_locals: Omitable[bool] = ...,
        log_message_format: Omitable[str | LoggingFormatter] = ...,
        columns: Omitable[Collection[str | RichProgressColumn]] = ...,
        transient: Omitable[bool] = ...,
        refresh_per_second: Omitable[float] = ...,
        speed_estimate_period: Omitable[float] = ...,
        default_column_markup: Omitable[bool] = ...,
    ):
        _branch_configure(
            self,
            config,
            markup=markup,
            highlighter=highlighter,
            width=width,
            height=height,
            emoji=emoji,
            color_system=color_system,
            theme=theme,
            soft_wrap=soft_wrap,
            force_terminal=force_terminal,
            force_jupyter=force_jupyter,
            force_interactive=force_interactive,
            level=level,
            show_level=show_level,
            show_time=show_time,
            show_path=show_path,
            log_time_format=log_time_format,
            omit_repeated_times=omit_repeated_times,
            rich_tracebacks=rich_tracebacks,
            tracebacks_show_locals=tracebacks_show_locals,
            log_message_format=log_message_format,
            columns=columns,
            transient=transient,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            default_column_markup=default_column_markup,
        )

    def branch_add(
        self,
        name: str,
        /,
        sink: Sink | None = None,
        *,
        markup: Omitable[bool] = ...,
        highlighter: Omitable[RichHighlighter] = ...,
        width: Omitable[int | None] = ...,
        height: Omitable[int | None] = ...,
        emoji: Omitable[bool] = ...,
        color_system: Omitable[Literal["auto", "standard", "truecolor"] | None] = ...,
        theme: Omitable[RichTheme] = ...,
        soft_wrap: Omitable[bool] = ...,
        force_terminal: Omitable[bool | None] = ...,
        force_jupyter: Omitable[bool | None] = ...,
        force_interactive: Omitable[bool | None] = ...,
        level: Omitable[str | int] = ...,
        show_level: Omitable[bool] = ...,
        show_time: Omitable[bool] = ...,
        show_path: Omitable[bool] = ...,
        log_time_format: Omitable[str | FormatTimeCallable] = ...,
        omit_repeated_times: Omitable[bool] = ...,
        rich_tracebacks: Omitable[bool] = ...,
        tracebacks_show_locals: Omitable[bool] = ...,
        log_message_format: Omitable[str | LoggingFormatter] = ...,
    ):
        _branch_add(
            self,
            name,
            sink=sink,
            markup=markup,
            highlighter=highlighter,
            width=width,
            height=height,
            emoji=emoji,
            color_system=color_system,
            theme=theme,
            soft_wrap=soft_wrap,
            force_terminal=force_terminal,
            force_jupyter=force_jupyter,
            force_interactive=force_interactive,
            level=level,
            show_level=show_level,
            show_time=show_time,
            show_path=show_path,
            log_time_format=log_time_format,
            omit_repeated_times=omit_repeated_times,
            rich_tracebacks=rich_tracebacks,
            tracebacks_show_locals=tracebacks_show_locals,
            log_message_format=log_message_format,
        )

    def branch_remove(
        self,
        name: str,
        /,
    ):
        _branch_remove(
            self,
            name,
        )

    def task_add(
        self,
        name: str,
        /,
        *,
        desc: str,
        total: float | None,
        done: float = 0,
    ):
        _task_add(
            self,
            name,
            desc=desc,
            total=total,
            done=done,
        )

    def task_remove(
        self,
        name: str,
        /,
    ):
        _task_remove(
            self,
            name,
        )

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _log(
            self,
            level,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def debug(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _debug(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def info(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _info(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def warn(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _warn(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def error(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _error(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def critical(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _critical(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def exception(
        self,
        msg: object,
        *args: object,
        log_options: LogOptions | None = None,
        console_options: ConsolePrintOptions | None = None,
    ):
        _exception(
            self,
            msg,
            *args,
            log_options=log_options,
            console_options=console_options,
        )

    def advance(
        self,
        name: str,
        /,
        value: float,
    ):
        _advance(
            self,
            name,
            advance=value,
        )

    def track(
        self,
        value: object,
        /,
        name: str | None,
        *,
        step: int | None,
        epoch: int | None,
        context: AimObject,
    ):
        _track(
            self,
            value,
            name=name,
            step=step,
            epoch=epoch,
            context=context,
        )

    def add_tag(
        self,
        name: str,
        /,
    ):
        _add_tag(
            self,
            name,
        )

    def remove_tag(
        self,
        name: str,
        /,
    ):
        _remove_tag(
            self,
            name,
        )

    def update_metadata(
        self,
        name: str,
        /,
        metadata: AimObject,
    ):
        _update_metadata(
            self,
            name,
            metadata,
        )


_current_shell_lock: threading.Lock = threading.Lock()
_current_shell: Shell | None = None


def get_global_shell(sink: Sink | Literal["stderr", "stdout"] = "stderr"):
    if nnlogging.shell._current_shell is None:
        with nnlogging.shell._current_shell_lock:
            shell = Shell()
            if isinstance(sink, str) and sink in ("stderr", "stdout"):
                sink = cast(Sink, getattr(sys, sink))
            shell.branch_add("default", sink)
            shell.debug(f'"global_shell" is now initialized as {repr(shell)}')
            nnlogging.shell._current_shell = shell
    return nnlogging.shell._current_shell


def replace_global_shell(shell: Shell):
    with nnlogging.shell._current_shell_lock:
        current_shell = nnlogging.shell._current_shell
        msg = f'"global_shell" has been replaced from {repr(current_shell)} to {repr(shell)}'
        if current_shell is not None:
            current_shell.info(msg)
        nnlogging.shell._current_shell = shell
        shell.debug(msg)
