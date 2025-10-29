import logging
from collections.abc import Collection
from dataclasses import asdict, dataclass, field
from logging import Formatter as LoggingFormatter
from typing import Literal

from aim import Repo as AimRepo, Run as AimRun
from rich.highlighter import Highlighter as RichHighlighter
from rich.progress import ProgressColumn as RichProgressColumn
from rich.theme import Theme as RichTheme

from nnlogging.typings import Branch, FormatTimeCallable, Omitable, Sink
from nnlogging.utils.helpers import evolve_, or_
from nnlogging.utils.rich_factories import (
    get_rich_console,
    get_rich_handler,
    get_rich_progress_default_columns,
)


@dataclass(slots=True, kw_only=True)
class LoggerConfig:
    name: str = "nnlogging"
    level: int | str = logging.DEBUG
    propagate: bool = False


def get_logging_logger(
    config: LoggerConfig | None = None,
    /,
    *,
    name: Omitable[str] = ...,
    level: Omitable[int | str] = ...,
    propagate: Omitable[bool] = ...,
):
    config_base = config or LoggerConfig()
    config_evolved = evolve_(
        config_base,
        name=name,
        level=level,
        propagate=propagate,
    )
    logger = logging.getLogger(config_evolved.name)
    logger.setLevel(config_evolved.level)
    logger.propagate = config_evolved.propagate
    return logger


@dataclass(slots=True, kw_only=True)
class RunConfig:
    experiment: str | None = None
    repo: str | AimRepo | None = None
    system_tracking_interval: float | None = 10
    capture_terminal_logs: bool = False
    log_system_params: bool = False
    run_hash: str | None = None
    read_only: bool = False
    force_resume: bool = False


def get_aim_run(
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
    config_base = config or RunConfig()
    config_evolved = evolve_(
        config_base,
        experiment=experiment,
        repo=repo,
        system_tracking_interval=system_tracking_interval,
        capture_terminal_logs=capture_terminal_logs,
        log_system_params=log_system_params,
        run_hash=run_hash,
        read_only=read_only,
        force_resume=force_resume,
    )
    run = AimRun(**asdict(config_evolved))  # pyright: ignore[reportAny]
    return run


@dataclass(slots=True, kw_only=True)
class BranchConfig:
    # shared
    markup: bool = True
    highlighter: RichHighlighter | None = None

    # console
    width: int | None = None
    height: int | None = None
    emoji: bool = True
    color_system: Literal["auto", "standard", "truecolor"] | None = "auto"
    theme: RichTheme | None = None
    soft_wrap: bool = True
    force_terminal: bool | None = None
    force_jupyter: bool | None = None
    force_interactive: bool | None = None

    # handler
    level: str | int = logging.NOTSET
    show_level: bool = True
    show_time: bool = True
    show_path: bool = True
    log_time_format: str | FormatTimeCallable = "[%x %X]"
    omit_repeated_times: bool = True
    rich_tracebacks: bool = True
    tracebacks_show_locals: bool = False
    log_message_format: str | LoggingFormatter = "%(message)s"

    # progress
    columns: Collection[str | RichProgressColumn] = field(
        default_factory=get_rich_progress_default_columns,
        compare=False,
    )
    transient: bool = False
    refresh_per_second: float = 10
    speed_estimate_period: float = 3600
    default_column_markup: bool = True


def get_branch(
    config: BranchConfig | None = None,
    /,
    sink: Sink | None = None,
    *,
    markup: Omitable[bool] = ...,
    highlighter: Omitable[RichHighlighter | None] = ...,
    width: Omitable[int | None] = ...,
    height: Omitable[int | None] = ...,
    emoji: Omitable[bool] = ...,
    color_system: Omitable[Literal["auto", "standard", "truecolor"] | None] = ...,
    theme: Omitable[RichTheme | None] = ...,
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
    if config is None:
        config = BranchConfig()
    console = get_rich_console(
        sink,
        width=or_(width, config.width),
        height=or_(height, config.height),
        markup=or_(markup, config.markup),
        emoji=or_(emoji, config.emoji),
        color_system=or_(color_system, config.color_system),
        theme=or_(theme, config.theme),
        highlighter=or_(highlighter, config.highlighter),
        soft_wrap=or_(soft_wrap, config.soft_wrap),
        force_terminal=or_(force_terminal, config.force_terminal),
        force_jupyter=or_(force_jupyter, config.force_jupyter),
        force_interactive=or_(force_interactive, config.force_interactive),
    )
    handler = get_rich_handler(
        console,
        level=or_(level, config.level),
        show_level=or_(show_level, config.show_level),
        show_time=or_(show_time, config.show_time),
        show_path=or_(show_path, config.show_path),
        log_time_format=or_(log_time_format, config.log_time_format),
        omit_repeated_times=or_(omit_repeated_times, config.omit_repeated_times),
        markup=or_(markup, config.markup),
        highlighter=or_(highlighter, config.highlighter),
        rich_tracebacks=or_(rich_tracebacks, config.rich_tracebacks),
        tracebacks_show_locals=or_(
            tracebacks_show_locals, config.tracebacks_show_locals
        ),
        log_message_format=or_(log_message_format, config.log_message_format),
    )
    return Branch(
        console=console,
        handler=handler,
        tasks=dict(),
        progress=None,
    )
