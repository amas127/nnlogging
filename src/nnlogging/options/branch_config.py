from dataclasses import dataclass

from .rich_console import RichConsoleOption, RichConsoleOptionDict
from .rich_handler import RichHandlerOption, RichHandlerOptionDict
from .rich_progress import RichProgressOption, RichProgressOptionDict


@dataclass(kw_only=True)
class BranchConfigOption(RichConsoleOption, RichHandlerOption, RichProgressOption):
    def __post_init__(self):
        RichConsoleOption.__post_init__(self)
        RichHandlerOption.__post_init__(self)


class BranchConfigOptionDict(
    RichConsoleOptionDict,
    RichHandlerOptionDict,
    RichProgressOptionDict,
): ...
