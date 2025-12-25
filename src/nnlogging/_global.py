from collections.abc import Collection

from nnlogging.helpers import inc_stacklevel
from nnlogging.options import (
    BranchParOpt,
    CapexcParOpt,
    CapwarnParOpt,
    ConsoleParOpt,
    FilterParOpt,
    HandlerParOpt,
    LogParOpt,
    LoggerParOpt,
    ProgressParOpt,
    RenderParOpt,
    RunParOpt,
    TaskParOpt,
)
from nnlogging.shell import Shell
from nnlogging.typings import (
    Artifact,
    Jsonlike,
    Level,
    RichConsoleRenderable,
    Sink,
    StrPath,
    Unpack,
)


__all__ = [
    "add_branch",
    "add_task",
    "advance",
    "capture_warnings",
    "configure_capture_exception",
    "configure_capture_warning",
    "configure_console",
    "configure_filter",
    "configure_handler",
    "configure_log",
    "configure_logger",
    "configure_progress",
    "configure_render",
    "configure_run",
    "critical",
    "debug",
    "error",
    "exception",
    "info",
    "log",
    "remove_branch",
    "remove_task",
    "render",
    "replace_global_shell",
    "track",
    "track_artifact",
    "warning",
]

_global_shell: Shell = Shell("_global_")


def replace_global_shell(shell: Shell) -> Shell:
    global _global_shell  # noqa: PLW0603
    orig_shell = _global_shell
    _global_shell = shell
    return orig_shell


def configure_console(**kwargs: Unpack[ConsoleParOpt]) -> None:
    _global_shell.configure_console(**kwargs)


def configure_handler(**kwargs: Unpack[HandlerParOpt]) -> None:
    _global_shell.configure_handler(**kwargs)


def configure_filter(**kwargs: Unpack[FilterParOpt]) -> None:
    _global_shell.configure_filter(**kwargs)


def configure_progress(**kwargs: Unpack[ProgressParOpt]) -> None:
    _global_shell.configure_progress(**kwargs)


def configure_log(**kwargs: Unpack[LogParOpt]) -> None:
    _global_shell.configure_log(**kwargs)


def configure_render(**kwargs: Unpack[RenderParOpt]) -> None:
    _global_shell.configure_render(**kwargs)


def configure_capture_warning(**kwargs: Unpack[CapwarnParOpt]) -> None:
    _global_shell.configure_capture_warning(**kwargs)


def configure_capture_exception(**kwargs: Unpack[CapexcParOpt]) -> None:
    _global_shell.configure_capture_exception(**kwargs)


def configure_logger(
    loggers: Collection[str | None], **kwargs: Unpack[LoggerParOpt]
) -> None:
    _global_shell.configure_logger(loggers, **kwargs)


def configure_run(**kwargs: Unpack[RunParOpt]) -> None:
    _global_shell.configure_run(**kwargs)


def add_branch(
    logger: str | None = None, *sinks: tuple[str, Sink], **kwargs: Unpack[BranchParOpt]
) -> None:
    _global_shell.add_branch(logger, *sinks, **kwargs)


def remove_branch(*names: str) -> None:
    _global_shell.remove_branch(*names)


def add_task(name: str, **kwargs: Unpack[TaskParOpt]) -> None:
    _global_shell.add_task(name, **kwargs)


def remove_task(name: str) -> None:
    _global_shell.remove_task(name)


def advance(task: str, value: float) -> None:
    _global_shell.advance(task, value)


def log(
    logger: str | None,
    level: Level,
    msg: str,
    *args: object,
    **kwargs: Unpack[LogParOpt],
) -> None:
    _global_shell.log(
        logger, level, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def debug(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.debug(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def info(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.info(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def warning(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.warning(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def error(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.error(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def critical(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.critical(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def exception(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:
    _global_shell.exception(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def render(
    logger: str | None,
    level: str | int,
    *objs: RichConsoleRenderable,
    **kwargs: Unpack[RenderParOpt],
) -> None:
    _global_shell.render(logger, level, *objs, **kwargs)


def capture_warnings(**kwargs: Unpack[CapwarnParOpt]) -> None:
    _global_shell.capture_warnings(**kwargs)


def track(
    step: int,
    metrics: Jsonlike | None = None,
    artifacts: list[Artifact] | None = None,
    context: Jsonlike | None = None,
) -> None:
    _global_shell.track(step, metrics, artifacts, context)


def track_artifact(step: int, *paths: StrPath, context: Jsonlike | None = None) -> None:
    _global_shell.track_artifact(step, *paths, context=context)
