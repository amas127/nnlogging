from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypedDict

from nnlogging.typings import RichHighlighter, RichNullHighlighter, RichTheme


__all__ = ["ConsoleFullOpt", "ConsoleParOpt"]


@dataclass(kw_only=True)
class ConsoleFullOpt:
    width: int | None = field(default=None)
    height: int | None = field(default=None)
    markup: bool = field(default=True)
    emoji: bool = field(default=True)
    color_system: Literal["auto", "standard", "256", "truecolor"] | None = field(
        default="auto"
    )
    theme: RichTheme | None = field(default=None)
    highlighter: RichHighlighter = field(default_factory=RichNullHighlighter)
    soft_wrap: bool = field(default=False)
    force_terminal: bool | None = field(default=None)
    force_jupyter: bool | None = field(default=None)
    force_interactive: bool | None = field(default=None)


class ConsoleParOpt(TypedDict, total=False):
    width: int | None
    height: int | None
    markup: bool
    emoji: bool
    color_system: Literal["auto", "standard", "256", "truecolor"] | None
    theme: RichTheme | None
    highlighter: RichHighlighter
    soft_wrap: bool
    force_terminal: bool | None
    force_jupyter: bool | None
    force_interactive: bool | None
