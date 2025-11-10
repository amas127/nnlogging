from datetime import datetime
from os import PathLike
from typing import Callable, TypeAlias, TypedDict

from rich.console import Console as RichConsole
from rich.logging import RichHandler
from rich.progress import Progress as RichProgress, TaskID as RichTaskID
from rich.text import Text as RichText

StrPath: TypeAlias = str | PathLike[str]
FormatTimeCallable: TypeAlias = Callable[[datetime], RichText]


class Branch(TypedDict, total=True):
    console: RichConsole
    handler: RichHandler
    tasks: dict[str, RichTaskID]
    progress: RichProgress | None
