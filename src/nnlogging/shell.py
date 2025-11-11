from logging import Logger as LoggingLogger
from typing import Literal

from aim import Run as AimRun
from aim.storage.types import AimObject

import nnlogging.shell_funcs as f
from nnlogging.options import (
    BranchConfigOption,
    BranchConfigOptionDict,
    LoggerConfigOption,
    LoggerConfigOptionDict,
    LogOptionDict,
    RunConfigOption,
    RunConfigOptionDict,
    TaskOptionDict,
    TrackOptionDict,
)
from nnlogging.typings.aliases import Branch
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import Sink


class Shell:
    def __init__(
        self,
        shell_name: str = "nnlogging",
        /,
        *,
        logger_config: LoggerConfigOption | None = None,
        run_config: RunConfigOption | None = None,
        branch_config: BranchConfigOption | None = None,
        strict: bool = False,
    ):
        self.logger: LoggingLogger | None = None
        self.run: AimRun | None = None
        self.branches: dict[str, Branch] = dict()

        self.name: str = shell_name
        self.logger_config: LoggerConfigOption = logger_config or LoggerConfigOption(
            name=shell_name
        )
        self.run_config: RunConfigOption = run_config or RunConfigOption()
        self.branch_config: BranchConfigOption = branch_config or BranchConfigOption()

        self.strict: bool = strict

    def logger_configure(
        self,
        **kwargs: Unpack[LoggerConfigOptionDict],
    ):
        f.logger_configure(
            self,
            **kwargs,
        )

    def run_configure(
        self,
        **kwargs: Unpack[RunConfigOptionDict],
    ):
        f.run_configure(
            self,
            **kwargs,
        )

    def branch_configure(
        self,
        **kwargs: Unpack[BranchConfigOptionDict],
    ):
        f.branch_configure(
            self,
            **kwargs,
        )

    def branch_add(
        self,
        name: str,
        /,
        sink: Sink | Literal["stderr", "stdout"] = "stderr",
        **kwargs: Unpack[BranchConfigOptionDict],
    ):
        f.branch_add(
            self,
            name,
            sink=sink,
            **kwargs,
        )

    def branch_remove(
        self,
        name: str,
        /,
    ):
        f.branch_remove(
            self,
            name,
        )

    def task_add(
        self,
        name: str,
        /,
        **kwargs: Unpack[TaskOptionDict],
    ):
        f.task_add(
            self,
            name,
            **kwargs,
        )

    def task_remove(
        self,
        name: str,
        /,
    ):
        f.task_remove(
            self,
            name,
        )

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.log(
            self,
            level,
            msg,
            *args,
            **kwargs,
        )

    def debug(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.debug(
            self,
            msg,
            *args,
            **kwargs,
        )

    def info(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.info(
            self,
            msg,
            *args,
            **kwargs,
        )

    def warn(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.warn(
            self,
            msg,
            *args,
            **kwargs,
        )

    def error(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.error(
            self,
            msg,
            *args,
            **kwargs,
        )

    def critical(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.critical(
            self,
            msg,
            *args,
            **kwargs,
        )

    def exception(
        self,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ):
        kwargs["stacklevel"] = kwargs.get("stacklevel", 2)
        f.exception(
            self,
            msg,
            *args,
            **kwargs,
        )

    def advance(self, name: str, value: float):
        f.advance(
            self,
            name,
            value,
        )

    def track(
        self,
        value: object,
        /,
        **kwargs: Unpack[TrackOptionDict],
    ):
        f.track(
            self,
            value,
            **kwargs,
        )

    def add_tag(
        self,
        tag: str,
        /,
    ):
        f.add_tag(
            self,
            tag,
        )

    def remove_tag(
        self,
        tag: str,
        /,
    ):
        f.remove_tag(
            self,
            tag,
        )

    def update_metadata(
        self,
        key: str,
        value: AimObject,
    ):
        f.update_metadata(
            self,
            key,
            value,
        )
