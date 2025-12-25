import datetime
from collections.abc import Callable
from typing import Any, ParamSpec, Protocol, TypeAlias, TypeVar, overload

from nnlogging.options import LogFullOpt, LogParOpt
from nnlogging.typings import (
    Artifact,
    DataclassInstance,
    DuckConnection,
    ExcInfoType,
    FilterExt,
    Jsonlike,
    Level,
    LogRecord,
    StrPath,
    TypeVarTuple,
    Unpack,
)

def get_level(lvl: Level, /) -> int: ...

_LogDictT = TypeVar("_LogDictT", bound=LogFullOpt | LogParOpt | dict[str, Any])

def inc_stacklevel(dct: _LogDictT, /, *, inc: int = 1) -> _LogDictT: ...
def inj_excinfo(dct: _LogDictT, /, *, exc: ExcInfoType = True) -> _LogDictT: ...
def asdict(d: DataclassInstance, /) -> dict[str, Any]: ...

_P = ParamSpec("_P")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_R = TypeVar("_R")
_Ts = TypeVarTuple("_Ts")

class _EmptyCompose(Protocol):
    @overload
    def __call__(self) -> None: ...
    @overload
    def __call__(self, arg: _T1) -> _T1: ...
    @overload
    def __call__(
        self, arg1: _T1, arg2: _T2, *args: Unpack[_Ts]
    ) -> tuple[_T1, _T2, Unpack[_Ts]]: ...

@overload
def compose() -> _EmptyCompose: ...
@overload
def compose(f: Callable[_P, _R]) -> Callable[_P, _R]: ...
@overload
def compose(f2: Callable[[_T1], _R], f1: Callable[_P, _T1]) -> Callable[_P, _R]: ...
@overload
def compose(
    f3: Callable[[_T2], _R], f2: Callable[[_T1], _T2], f1: Callable[_P, _T1]
) -> Callable[_P, _R]: ...
def get_duckcon(con: StrPath | DuckConnection | None = None) -> DuckConnection: ...
@overload
def dumps(o: Jsonlike, /) -> str: ...
@overload
def dumps(artifact: Artifact, /) -> str: ...
@overload
def dumps(artifacts: list[Artifact], /) -> str: ...
@overload
def dumps(o: None, /) -> None: ...

Loadable: TypeAlias = bytes | bytearray | str | memoryview[int]
NestLoadable: TypeAlias = (
    Loadable | tuple[NestLoadable, ...] | list[NestLoadable] | dict[Any, NestLoadable]
)

@overload
def loads(o: Loadable, /) -> Any: ...  # noqa: ANN401
@overload
def loads(o: NestLoadable, /) -> Any: ...  # noqa: ANN401
@overload
def loads(o: _R, /) -> _R: ...
def now() -> datetime.datetime: ...
def filtlog(fltr: FilterExt, record: LogRecord) -> bool: ...
