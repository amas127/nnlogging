from collections.abc import Collection
from logging import Formatter as LoggingFormatter
from typing import Literal

from rich.highlighter import Highlighter as RichHighlighter
from rich.progress import ProgressColumn as RichProgressColumn
from rich.theme import Theme as RichTheme

from nnlogging.shell_protocol import ShellProtocol
from nnlogging.typings import FormatTimeCallable, Omitable, Sink
from nnlogging.utils.exception import (
    raise_branch_exists_error,
    raise_branch_not_found_error,
)
from nnlogging.utils.factory_funcs.shell_ import BranchConfig, get_branch
from nnlogging.utils.helpers import evolve_


def branch_configure(
    inst: ShellProtocol,
    /,
    config: BranchConfig | None = None,
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
    inst.branch_config = evolve_(
        config or inst.branch_config,
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
    inst: ShellProtocol,
    /,
    name: str,
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
    if name in inst.branches:
        raise_branch_exists_error(
            inst,
            name,
            stacklevel=6,
        )
    else:
        branch = get_branch(
            inst.branch_config,
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
        inst.branches[name] = branch
        if inst.logger is not None:
            # TODO: add branch-add-hint
            inst.logger.addHandler(branch["handler"])


def branch_remove(
    inst: ShellProtocol,
    /,
    name: str,
):
    if name not in inst.branches:
        raise_branch_not_found_error(
            inst,
            name,
            stacklevel=6,
        )
    else:
        branch = inst.branches[name]
        branch["handler"].close()
        branch["tasks"].clear()
        if branch["progress"] is not None:
            branch["progress"].stop()
        if inst.logger is not None:
            # TODO: add branch-remove-hint
            inst.logger.removeHandler(branch["handler"])
        del inst.branches[name]
