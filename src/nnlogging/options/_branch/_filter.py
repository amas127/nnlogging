from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict


if TYPE_CHECKING:
    from collections.abc import Collection

    from nnlogging.typings import LogFilter

__all__ = ["FilterFullOpt", "FilterParOpt"]


@dataclass(kw_only=True)
class FilterFullOpt:
    filter: LogFilter | Collection[LogFilter] | None = field(default=None)


class FilterParOpt(TypedDict, total=False):
    filter: LogFilter | Collection[LogFilter] | None
