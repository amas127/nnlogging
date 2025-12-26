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
    Status,
    StrPath,
    Unpack,
)


__all__ = [
    "add_branch",
    "add_extras",
    "add_hparams",
    "add_summaries",
    "add_tags",
    "add_task",
    "advance",
    "archive_run",
    "capture_warnings",
    "close_run",
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
    "remove_tags",
    "remove_task",
    "render",
    "replace_global_shell",
    "track",
    "track_artifact",
    "update_status",
    "warning",
]

_global_shell: Shell = Shell("_global_")


def replace_global_shell(shell: Shell) -> Shell:
    with shell.lock:
        global _global_shell  # noqa: PLW0603
        orig_shell = _global_shell
        _global_shell = shell
        return orig_shell


def configure_console(**kwargs: Unpack[ConsoleParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_console(**kwargs)


def configure_handler(**kwargs: Unpack[HandlerParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_handler(**kwargs)


def configure_filter(**kwargs: Unpack[FilterParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_filter(**kwargs)


def configure_progress(**kwargs: Unpack[ProgressParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_progress(**kwargs)


def configure_log(**kwargs: Unpack[LogParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_log(**kwargs)


def configure_render(**kwargs: Unpack[RenderParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_render(**kwargs)


def configure_capture_warning(
    **kwargs: Unpack[CapwarnParOpt],
) -> None:  # pragma: no cover
    _global_shell.configure_capture_warning(**kwargs)


def configure_capture_exception(
    **kwargs: Unpack[CapexcParOpt],
) -> None:  # pragma: no cover
    _global_shell.configure_capture_exception(**kwargs)


def configure_logger(
    loggers: Collection[str | None], **kwargs: Unpack[LoggerParOpt]
) -> None:  # pragma: no cover
    _global_shell.configure_logger(loggers, **kwargs)


def configure_run(**kwargs: Unpack[RunParOpt]) -> None:  # pragma: no cover
    _global_shell.configure_run(**kwargs)


def add_branch(
    *sinks: tuple[str, Sink], logger: str | None = None, **kwargs: Unpack[BranchParOpt]
) -> None:  # pragma: no cover
    _global_shell.add_branch(*sinks, logger=logger, **kwargs)


def remove_branch(*names: str) -> None:  # pragma: no cover
    _global_shell.remove_branch(*names)


def add_task(name: str, **kwargs: Unpack[TaskParOpt]) -> None:  # pragma: no cover
    _global_shell.add_task(name, **kwargs)


def remove_task(name: str) -> None:  # pragma: no cover
    _global_shell.remove_task(name)


def advance(task: str, value: float) -> None:  # pragma: no cover
    _global_shell.advance(task, value)


def log(
    logger: str | None,
    level: Level,
    msg: str,
    *args: object,
    **kwargs: Unpack[LogParOpt],
) -> None:  # pragma: no cover
    _global_shell.log(
        logger, level, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def debug(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.debug(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def info(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.info(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def warning(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.warning(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def error(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.error(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def critical(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.critical(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def exception(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None:  # pragma: no cover
    _global_shell.exception(
        logger, msg, *args, **inc_stacklevel(LogParOpt(stacklevel=1) | kwargs)
    )


def render(
    logger: str | None,
    level: str | int,
    *objs: RichConsoleRenderable,
    **kwargs: Unpack[RenderParOpt],
) -> None:  # pragma: no cover
    _global_shell.render(logger, level, *objs, **kwargs)


def capture_warnings(**kwargs: Unpack[CapwarnParOpt]) -> None:
    _global_shell.capture_warnings(**kwargs)


def add_tags(*tags: str) -> None:
    _global_shell.add_tags(*tags)


def remove_tags(*tags: str) -> None:
    _global_shell.remove_tags(*tags)


def add_hparams(hparams: Jsonlike) -> None:
    _global_shell.add_hparams(hparams)


def add_summaries(summaries: Jsonlike) -> None:
    _global_shell.add_summaries(summaries)


def add_extras(extras: Jsonlike) -> None:
    _global_shell.add_extras(extras)


def track(
    step: int,
    metrics: Jsonlike | None = None,
    artifacts: list[Artifact] | None = None,
    context: Jsonlike | None = None,
) -> None:  # pragma: no cover
    _global_shell.track(step, metrics, artifacts, context)


def track_artifact(
    step: int, *paths: StrPath, context: Jsonlike | None = None
) -> None:  # pragma: no cover
    _global_shell.track_artifact(step, *paths, context=context)


def update_status(status: Status) -> None:
    _global_shell.update_status(status)


def close_run() -> None:
    _global_shell.close_run()


def archive_run() -> None:
    _global_shell.archive_run()
