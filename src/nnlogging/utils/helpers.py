import threading
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from nnlogging.options import (
    LoggingLogOptionDict,
    LogOptionDict,
    RichConsoleOptionDict,
    RichHandlerOptionDict,
    RichPrintOptionDict,
    RichProgressOptionDict,
)


def get_name(
    inst: object,
    /,
) -> object:
    return getattr(inst, "name", inst)


LogOptionT = TypeVar(
    "LogOptionT",
    bound=LogOptionDict | LoggingLogOptionDict | dict[str, Any],
)


def inc_stacklevel(
    dct: LogOptionT,
    /,
) -> LogOptionT:
    if "stacklevel" in dct:
        dct["stacklevel"] = dct["stacklevel"] + 1
    return dct


def inject_excinfo(
    dct: LogOptionT,
    e: BaseException | bool = True,
    /,
) -> LogOptionT:
    if "exc_info" not in dct:
        dct["exc_info"] = e
    return dct


TypedDictT = TypeVar(
    "TypedDictT",
    bound=RichConsoleOptionDict
    | RichHandlerOptionDict
    | RichProgressOptionDict
    | LoggingLogOptionDict
    | RichPrintOptionDict,
)


def filter_by_typeddict(
    dct: Mapping[str, object],
    /,
    typpeddict: type[TypedDictT],
) -> TypedDictT:
    keys = typpeddict.__annotations__.keys()
    return cast(TypedDictT, {k: v for k, v in dct.items() if k in keys})  # pyright: ignore[reportInvalidCast]


def with_lock(lock: threading.Lock):
    def decorator(f):
        def wrapper(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)

        return wrapper

    return decorator
