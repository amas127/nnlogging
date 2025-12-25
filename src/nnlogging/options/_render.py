from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.typings import RichJustifyMethod, RichOverflowMethod, RichStyle


__all__ = ["RenderFullOpt", "RenderParOpt"]


@dataclass(kw_only=True)
class RenderFullOpt:
    sep: str = field(default=" ")
    end: str = field(default="\n")
    style: str | RichStyle | None = field(default=None)
    justify: RichJustifyMethod | None = field(default=None)
    overflow: RichOverflowMethod | None = field(default=None)
    new_line_start: bool = field(default=False)
    crop: bool = field(default=False)
    no_wrap: bool | None = field(default=True)
    soft_wrap: bool | None = field(default=None)
    emoji: bool | None = field(default=None)
    markup: bool | None = field(default=None)
    highlight: bool | None = field(default=None)
    width: int | None = field(default=None)
    height: int | None = field(default=None)


class RenderParOpt(TypedDict, total=False):
    sep: str
    end: str
    style: str | RichStyle | None
    justify: RichJustifyMethod | None
    overflow: RichOverflowMethod | None
    crop: bool
    new_line_start: bool
    no_wrap: bool | None
    soft_wrap: bool | None
    emoji: bool | None
    markup: bool | None
    highlight: bool | None
    width: int | None
    height: int | None
