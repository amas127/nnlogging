from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING, Any

import duckdb
import orjson

from nnlogging.exceptions import (
    LevelNameNotFoundError,
    LevelTypeWeirdError,
    StacklevelTypeWeirdError,
)
from nnlogging.typings import (
    DataclassInstance,
    DuckConnection,
    FilterCallable,
    FilterFilterable,
    Jsonlike,
    LogRecord,
)


if TYPE_CHECKING:
    from collections.abc import Callable

    from nnlogging.typings import ExcInfoType, StrPath


def get_level(o: Any, /) -> int:  # noqa: ANN401
    match o:
        case int():
            return o
        case str():
            if isinstance(lvl := logging._nameToLevel.get(o.upper()), int):  # noqa: SLF001
                return lvl
            raise LevelNameNotFoundError(o)
    raise LevelTypeWeirdError(o)


def inc_stacklevel(dct: Any, /, *, inc: int = 1) -> Any:  # noqa: ANN401
    match dct:
        case dict():
            if (lvl := dct.get("stacklevel")) is not None:
                if not isinstance(lvl, int):
                    raise StacklevelTypeWeirdError(lvl)
                dct["stacklevel"] = lvl + inc
        case DataclassInstance():
            if hasattr(dct, "stacklevel"):
                dct.stacklevel += inc  # pyright: ignore[reportAttributeAccessIssue]
    return dct


def inj_excinfo(dct: Any, /, *, exc: ExcInfoType = True) -> Any:  # noqa: ANN401
    match dct:
        case dict():
            if dct.get("exc_info") is None:  # NOTE: allow to refuse with `False`
                dct["exc_info"] = exc
        case DataclassInstance():
            if hasattr(dct, "exc_info") and dct.exc_info is None:  # pyright: ignore[reportAttributeAccessIssue]
                dct.exc_info = exc  # pyright: ignore[reportAttributeAccessIssue]
    return dct


def asdict(m: DataclassInstance, /) -> dict[str, Any]:
    if hasattr(m, "__slots__"):
        return {k: getattr(m, k) for k in m.__slots__}  # pyright: ignore[reportAttributeAccessIssue]
    return m.__dict__.copy()


def compose(*fs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    if len(fs) == 0:

        def empty_compose(*args: Any) -> Any:  # noqa: ANN401
            if len(args) == 0:
                return None
            if len(args) == 1:
                return args[0]
            return args

        return empty_compose

    def multi_compose(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        nargs, nkwargs = args, kwargs
        for f in reversed(fs):
            if not isinstance(nargs, tuple):
                nargs = (nargs,)
            nargs, nkwargs = f(*nargs, **nkwargs), {}
        return nargs

    return multi_compose


def get_duckcon(
    con: StrPath | DuckConnection | None = None,
) -> DuckConnection:  # pragma: no cover
    if not isinstance(con, DuckConnection):
        con = duckdb.connect(con or ":memory:")  # pyright: ignore[reportArgumentType]
    return con


def dumps(o: Jsonlike | None) -> str | None:
    if o is None:
        return None
    return orjson.dumps(
        o, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_UUID
    ).decode()


def loads(o: Any) -> Any:  # noqa: ANN401
    match o:
        case bytes() | bytearray() | str() | memoryview():
            return orjson.loads(o)
        case tuple():
            return tuple(loads(i) for i in o)
        case list():
            return [loads(i) for i in o]
        case dict():
            return {k: loads(v) for k, v in o.items()}
    return o


def now() -> datetime.datetime:  # pragma: no cover
    return (
        datetime.datetime.now().astimezone(datetime.timezone.utc).replace(tzinfo=None)
    )


def filtlog(fltr: Any, record: LogRecord) -> bool:  # pragma: no cover  # noqa: ANN401
    match fltr:
        case FilterFilterable():
            return fltr.filter(record)
        case FilterCallable():
            return fltr(record)
        case _:
            raise TypeError
