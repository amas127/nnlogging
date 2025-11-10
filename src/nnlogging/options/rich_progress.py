from collections.abc import Collection
from dataclasses import dataclass, field
from typing import TypedDict

from rich.progress import ProgressColumn as RichProgressColumn


def get_default_progress_columns():
    from rich.progress import (
        BarColumn,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeRemainingColumn,
    )

    spinner_column = SpinnerColumn(
        spinner_name="dots",
        style="progress.spinner",
        finished_text=" ",
    )
    text_column = TextColumn(
        text_format="{task.description}",
        style="progress.description",
        justify="left",
    )
    bar_column = BarColumn(bar_width=40)
    task_progress_column = TaskProgressColumn(
        text_format="{task.percentage:>3.0f}%",
        text_format_no_percentage="",
        style="progress.percentage",
        justify="right",
        show_speed=True,
    )
    time_remaining_column = TimeRemainingColumn(
        compact=False,
        elapsed_when_finished=True,
    )
    return (
        spinner_column,
        text_column,
        bar_column,
        task_progress_column,
        time_remaining_column,
    )


@dataclass(kw_only=True)
class RichProgressOption:
    columns: Collection[str | RichProgressColumn] = field(
        default_factory=get_default_progress_columns
    )
    transient: bool = field(default=False)
    refresh_per_second: float = field(default=10)
    speed_estimate_period: float = field(default=3600)


class RichProgressOptionDict(TypedDict, total=False):
    columns: Collection[str | RichProgressColumn]
    transient: bool
    refresh_per_second: float
    speed_estimate_period: float
