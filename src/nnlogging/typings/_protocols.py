from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Literal,
    Protocol,
    TextIO,
    TypeAlias,
    TypedDict,
    runtime_checkable,
)


if TYPE_CHECKING:
    from dataclasses import Field

    from ._exts import ExcInfoType, NotRequired
    from ._log import LogRecord, WarnMsg
    from ._rich import RichConsole, RichHandler, RichProgress, RichTaskID


@runtime_checkable
class Writable(Protocol):
    def write(self, text: str, /) -> int: ...
    def flush(self) -> None: ...


@runtime_checkable
class TerminalWritable(Protocol):
    def write(self, text: str, /) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...


Sink: TypeAlias = Literal["stderr", "stdout"] | Writable | TerminalWritable


@runtime_checkable
class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class Branch(TypedDict, total=True):
    console: RichConsole
    logger: str
    handler: RichHandler
    filter: FilterExt | list[FilterExt] | None
    tasks: dict[str, RichTaskID]
    progress: NotRequired[RichProgress]


Branches: TypeAlias = dict[str, Branch]


@runtime_checkable
class MsgCallback(Protocol):
    def __call__(self, msg: str, *args: object) -> None: ...


@runtime_checkable
class WarnCallback(Protocol):
    def __call__(self, warn: str, *args: object) -> None: ...


@runtime_checkable
class ExcCallback(Protocol):
    def __call__(self, msg: str, *args: object, exc_info: ExcInfoType) -> None: ...


@runtime_checkable
class WarnFormatter(Protocol):
    def __call__(self, warning: WarnMsg, /) -> str: ...


@runtime_checkable
class WarnCapturer(Protocol):
    def __call__(  # noqa: PLR0913, PLR0917
        self,
        message: Warning | str,
        category: type[Warning],
        filename: str,
        lineno: int,
        file: TextIO | None = None,
        line: str | None = None,
        source: Any | None = None,  # noqa: ANN401
    ) -> None: ...


@runtime_checkable
class FilterCallable(Protocol):
    def __call__(self, record: LogRecord, /) -> bool: ...


@runtime_checkable
class FilterFilterable(Protocol):
    def filter(self, record: LogRecord, /) -> bool: ...


FilterExt: TypeAlias = FilterCallable | FilterFilterable
