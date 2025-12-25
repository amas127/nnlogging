from nnlogging.helpers import asdict
from nnlogging.options import RenderFullOpt
from nnlogging.typings import Branches, Logger, RichConsoleRenderable
from nnlogging.utils import (
    get_activated_consoles,
    get_propagated_branches,
    mock_logrecord,
)


__all__ = ["render"]


def render(
    branches: Branches,
    logger: Logger,
    level: int,
    *objs: RichConsoleRenderable,
    kwargs: RenderFullOpt,
) -> None:
    record = mock_logrecord(logger, level)
    pbranches = get_propagated_branches(branches.values(), logger, level)
    aconsoles = get_activated_consoles(pbranches, record)
    for console in aconsoles:
        console.print(*objs, **asdict(kwargs))
