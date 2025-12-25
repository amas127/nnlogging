from dataclasses import dataclass, field
from typing import TypedDict


__all__ = ["CapexcFullOpt", "CapexcParOpt"]


@dataclass(kw_only=True)
class CapexcFullOpt:
    capture_internal_exception: bool = field(default=True)


class CapexcParOpt(TypedDict, total=False):
    capture_internal_exception: bool
