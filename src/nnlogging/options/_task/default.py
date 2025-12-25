from __future__ import annotations

from typing import TYPE_CHECKING

from rich.progress import (
    BarColumn,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)


if TYPE_CHECKING:
    from collections.abc import Sequence

    from nnlogging.typings import RichProgressColumn


def get_default_rich_progress_columns() -> Sequence[
    RichProgressColumn
]:  # pragma: no cover
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
