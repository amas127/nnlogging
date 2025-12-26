from collections.abc import Collection

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

_global_shell: Shell

def replace_global_shell(shell: Shell) -> Shell: ...
def configure_console(**kwargs: Unpack[ConsoleParOpt]) -> None: ...
def configure_handler(**kwargs: Unpack[HandlerParOpt]) -> None: ...
def configure_filter(**kwargs: Unpack[FilterParOpt]) -> None: ...
def configure_progress(**kwargs: Unpack[ProgressParOpt]) -> None: ...
def configure_log(**kwargs: Unpack[LogParOpt]) -> None: ...
def configure_render(**kwargs: Unpack[RenderParOpt]) -> None: ...
def configure_capture_warning(**kwargs: Unpack[CapwarnParOpt]) -> None: ...
def configure_capture_exception(**kwargs: Unpack[CapexcParOpt]) -> None: ...
def configure_logger(
    loggers: Collection[str | None], **kwargs: Unpack[LoggerParOpt]
) -> None: ...
def configure_run(**kwargs: Unpack[RunParOpt]) -> None: ...
def add_branch(
    *sinks: tuple[str, Sink], logger: str | None = None, **kwargs: Unpack[BranchParOpt]
) -> None: ...
def remove_branch(*names: str) -> None: ...
def add_task(name: str, **kwargs: Unpack[TaskParOpt]) -> None: ...
def remove_task(name: str) -> None: ...
def advance(task: str, value: float) -> None: ...
def log(
    logger: str | None,
    level: Level,
    msg: str,
    *args: object,
    **kwargs: Unpack[LogParOpt],
) -> None: ...
def debug(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def info(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def warning(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def error(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def critical(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def exception(
    logger: str | None, msg: str, *args: object, **kwargs: Unpack[LogParOpt]
) -> None: ...
def render(
    logger: str | None,
    level: str | int,
    *objs: RichConsoleRenderable,
    **kwargs: Unpack[RenderParOpt],
) -> None: ...
def capture_warnings(**kwargs: Unpack[CapwarnParOpt]) -> None: ...
def add_tags(*tags: str) -> None: ...
def remove_tags(*tags: str) -> None: ...
def add_hparams(hparams: Jsonlike) -> None: ...
def add_summaries(summaries: Jsonlike) -> None: ...
def add_extras(extras: Jsonlike) -> None: ...
def track(
    step: int,
    metrics: Jsonlike | None = None,
    artifacts: list[Artifact] | None = None,
    context: Jsonlike | None = None,
) -> None: ...
def track_artifact(
    step: int, *paths: StrPath, context: Jsonlike | None = None
) -> None: ...
def update_status(status: Status) -> None: ...
def close_run() -> None: ...
def archive_run() -> None: ...
