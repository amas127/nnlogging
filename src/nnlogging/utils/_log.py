from __future__ import annotations

import logging
from collections.abc import Collection
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from nnlogging.typings import FilterExt, LogFilter


__all__ = ["attach_handler_logfilter", "detach_handler_logfilter", "get_logfilter"]


def get_logfilter(
    fltr: LogFilter | Collection[LogFilter] | None,
) -> FilterExt | list[FilterExt] | None:
    match fltr:
        case None:
            return None
        case str():
            return logging.Filter(fltr)
        case logging.Filter():
            return fltr
        case Collection():
            return [get_logfilter(f) for f in fltr]  # pyright: ignore[reportReturnType]
        case _:
            raise TypeError


def attach_handler_logfilter(
    handler: logging.Handler, fltr: FilterExt | Collection[FilterExt] | None
) -> None:
    match fltr:
        case None:
            pass
        case logging.Filter():
            handler.addFilter(fltr)
        case Collection():
            for f in fltr:
                handler.addFilter(f)
        case _:
            raise TypeError


def detach_handler_logfilter(
    handler: logging.Handler, fltr: FilterExt | Collection[FilterExt] | None
) -> None:
    match fltr:
        case None:
            pass
        case logging.Filter():
            handler.removeFilter(fltr)
        case Collection():
            for f in fltr:
                handler.removeFilter(f)
        case _:
            raise TypeError
