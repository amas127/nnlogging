import threading
from typing import Literal

from aim.storage.types import AimObject

import nnlogging.shell_funcs as f
from nnlogging.options import (
    BranchConfigOptionDict,
    LoggerConfigOptionDict,
    LogOptionDict,
    RunConfigOptionDict,
    TaskOptionDict,
    TrackOptionDict,
)
from nnlogging.shell import Shell
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import Sink
from nnlogging.utils.helpers import with_lock

_global_shell_lock: threading.Lock = threading.Lock()
_global_shell: Shell = Shell("_global_")


__all__ = [
    "replace_global_shell",
    "logger_configure",
    "run_configure",
    "branch_configure",
    "branch_add",
    "branch_remove",
    "task_add",
    "task_remove",
    "log",
    "debug",
    "info",
    "warn",
    "error",
    "critical",
    "exception",
    "advance",
    "track",
    "add_tag",
    "remove_tag",
    "update_metadata",
]


@with_lock(_global_shell_lock)
def replace_global_shell(shell: Shell):
    global _global_shell, _global_shell_lock
    if _global_shell.logger is not None:
        _global_shell.logger_configure()
    if _global_shell.run is not None:
        _global_shell.run_configure()
    for name in list(_global_shell.branches.keys()):
        _global_shell.branch_remove(name)
    _global_shell = shell


@with_lock(_global_shell_lock)
def logger_configure(
    **kwargs: Unpack[LoggerConfigOptionDict],
):
    global _global_shell
    f.logger_configure(
        _global_shell,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def run_configure(
    **kwargs: Unpack[RunConfigOptionDict],
):
    global _global_shell
    f.run_configure(
        _global_shell,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def branch_configure(
    **kwargs: Unpack[BranchConfigOptionDict],
):
    global _global_shell
    f.branch_configure(
        _global_shell,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def branch_add(
    name: str,
    /,
    sink: Sink | Literal["stderr", "stdout"] = "stderr",
    **kwargs: Unpack[BranchConfigOptionDict],
):
    global _global_shell
    f.branch_add(
        _global_shell,
        name,
        sink=sink,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def branch_remove(
    name: str,
    /,
):
    global _global_shell
    f.branch_remove(
        _global_shell,
        name,
    )


@with_lock(_global_shell_lock)
def task_add(
    name: str,
    /,
    **kwargs: Unpack[TaskOptionDict],
):
    global _global_shell
    f.task_add(
        _global_shell,
        name,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def task_remove(
    name: str,
    /,
):
    global _global_shell
    f.task_remove(
        _global_shell,
        name,
    )


@with_lock(_global_shell_lock)
def log(
    level: int,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.log(
        _global_shell,
        level,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def debug(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.debug(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def info(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.info(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def warn(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.warn(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def error(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.error(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def critical(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.critical(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def exception(
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    global _global_shell
    kwargs["stacklevel"] = kwargs.get("stacklevel", 3)
    f.exception(
        _global_shell,
        msg,
        *args,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def advance(
    name: str,
    value: float,
):
    global _global_shell
    f.advance(
        _global_shell,
        name,
        value,
    )


@with_lock(_global_shell_lock)
def track(
    value: object,
    /,
    **kwargs: Unpack[TrackOptionDict],
):
    global _global_shell
    f.track(
        _global_shell,
        value,
        **kwargs,
    )


@with_lock(_global_shell_lock)
def add_tag(
    tag: str,
    /,
):
    global _global_shell
    f.add_tag(
        _global_shell,
        tag,
    )


@with_lock(_global_shell_lock)
def remove_tag(
    tag: str,
    /,
):
    global _global_shell
    f.remove_tag(
        _global_shell,
        tag,
    )


@with_lock(_global_shell_lock)
def update_metadata(
    key: str,
    value: AimObject,
):
    global _global_shell
    f.update_metadata(
        _global_shell,
        key,
        value,
    )
