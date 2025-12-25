from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict

from .default import get_default_rich_progress_columns


if TYPE_CHECKING:
    from collections.abc import Sequence

    from nnlogging.typings import RichProgressColumn


__all__ = ["ProgressFullOpt", "ProgressParOpt", "ProgressSetupFullOpt"]


@dataclass(kw_only=True)
class ProgressSetupFullOpt:
    transient: bool = field(default=False)
    refresh_per_second: float = field(default=10)
    speed_estimate_period: float = field(default=3600)
    expand: bool = field(default=False)
    redirect_stdout: bool = field(default=True)
    redirect_stderr: bool = field(default=True)


@dataclass(kw_only=True)
class ProgressFullOpt:
    setup: ProgressSetupFullOpt = field(default_factory=ProgressSetupFullOpt)
    columns: Sequence[RichProgressColumn] | None = field(default=None)

    def __post_init__(self) -> None:
        self.columns = self.columns or get_default_rich_progress_columns()


class ProgressParOpt(TypedDict, total=False):
    columns: Sequence[RichProgressColumn] | None
    transient: bool
    refresh_per_second: float
    speed_estimate_period: float
    expand: bool
    redirect_stdout: bool
    redirect_stderr: bool
