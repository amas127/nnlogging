from logging import Logger as LoggingLogger
from typing import Protocol, runtime_checkable

from aim import Run as AimRun
from aim.sdk.types import AimObject

from nnlogging.typings import Branch, LogOptions
from nnlogging.utils import BranchConfig, LoggerConfig, RunConfig


@runtime_checkable
class ShellProtocol(Protocol):
    logger_config: LoggerConfig
    run_config: RunConfig
    branch_config: BranchConfig
    logger: LoggingLogger | None
    run: AimRun | None
    branches: dict[str, Branch]

    def logger_configure(
        self,
        config: LoggerConfig | None,
        /,
    ): ...
    def run_configure(
        self,
        conf: RunConfig | None,
        /,
    ): ...
    def branch_configure(
        self,
        conf: BranchConfig | None,
        /,
    ): ...
    def branch_add(
        self,
        name: str,
        /,
    ): ...
    def branch_remove(
        self,
        name: str,
        /,
    ): ...
    def task_add(
        self,
        name: str,
        /,
        *,
        desc: str,
        total: float | None,
    ): ...
    def task_remove(
        self,
        name: str,
        /,
    ): ...
    def log(
        self,
        level: int,
        msg: object,
        /,
    ): ...
    def exception(
        self,
        msg: object,
        /,
        *,
        log_options: LogOptions | None = None,
    ): ...
    def advance(
        self,
        name: str,
        /,
        value: float,
    ): ...
    def track(
        self,
        value: object,
        /,
        name: str | None,
        *,
        step: int | None,
        epoch: int | None,
        context: AimObject,
    ): ...
