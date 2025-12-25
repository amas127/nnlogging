from ._console import ConsoleParOpt
from ._filter import FilterParOpt
from ._handler import HandlerParOpt


__all__ = ["BranchParOpt"]


class BranchParOpt(FilterParOpt, HandlerParOpt, ConsoleParOpt): ...
