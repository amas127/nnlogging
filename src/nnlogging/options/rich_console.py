from dataclasses import dataclass, field
from typing import Literal, TypedDict

from rich.highlighter import (
    Highlighter as RichHighlighter,
    NullHighlighter as RichNullHighlighter,
)
from rich.theme import Theme as RichTheme


@dataclass(kw_only=True)
class RichConsoleOption:
    width: int | None = field(default=None)
    height: int | None = field(default=None)
    markup: bool = field(default=True)
    emoji: bool = field(default=True)
    color_system: Literal["auto", "standard", "truecolor"] | None = field(
        default="auto"
    )
    theme: RichTheme | None = field(default=None)
    highlighter: RichHighlighter = field(default_factory=RichNullHighlighter)
    soft_wrap: bool = field(default=False)
    force_terminal: bool | None = field(default=None)
    force_jupyter: bool | None = field(default=None)
    force_interactive: bool | None = field(default=None)

    highlight: bool = field(init=False)

    def __post_init__(self):
        self.highlight = not isinstance(self.highlighter, RichNullHighlighter)


class RichConsoleOptionDict(TypedDict, total=False):
    width: int | None
    height: int | None
    markup: bool
    emoji: bool
    color_system: Literal["auto", "standard", "truecolor"] | None
    theme: RichTheme | None
    highlighter: RichHighlighter
    soft_wrap: bool
    force_terminal: bool | None
    force_jupyter: bool | None
    force_interactive: bool | None
