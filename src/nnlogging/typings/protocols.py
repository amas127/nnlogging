from logging import Logger as LoggingLogger
from typing import Protocol, TypeAlias, runtime_checkable

from aim import Run as AimRun

from nnlogging.options import (
    BranchConfigOption,
    LoggerConfigOption,
    LogOptionDict,
    RunConfigOption,
)
from nnlogging.typings.aliases import Branch
from nnlogging.typings.exts import Unpack


@runtime_checkable
class Writable(Protocol):
    def write(self, text: str, /) -> int: ...
    def flush(self) -> None: ...


@runtime_checkable
class TerminalWritable(Protocol):
    def write(self, text: str, /) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...


Sink: TypeAlias = Writable | TerminalWritable


class ExceptionProtocol(Protocol):
    branches: dict[str, Branch]

    def exception(
        self, msg: str, /, *args: object, **kwargs: Unpack[LogOptionDict]
    ): ...


class ShellProtocol(ExceptionProtocol, Protocol):
    name: str
    logger: LoggingLogger | None
    run: AimRun | None
    branches: dict[str, Branch]
    logger_config: LoggerConfigOption
    run_config: RunConfigOption
    branch_config: BranchConfigOption
    strict: bool

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        **kwargs: Unpack[LogOptionDict],
    ): ...
