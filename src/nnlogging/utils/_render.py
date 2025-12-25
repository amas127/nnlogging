from __future__ import annotations

import logging
from collections.abc import Collection
from typing import TYPE_CHECKING

from nnlogging.helpers import filtlog
from nnlogging.typings import FilterCallable, FilterFilterable


if TYPE_CHECKING:
    from nnlogging.typings import Branch, LogRecord, Logger, RichConsole

__all__ = ["get_activated_consoles", "get_propagated_branches", "mock_logrecord"]


def mock_logrecord(logger: Logger, level: int) -> LogRecord:
    # MAYBE: pretend to have a logrecord, maybe modified in the future
    return logging.makeLogRecord({"name": logger.name, "levelno": level})


def get_propagated_branches(
    branches: Collection[Branch], logger: Logger, level: int
) -> list[Branch]:
    if not logger.isEnabledFor(level):
        return []
    ploggers: set[str] = set()
    while logger:
        ploggers.add(logger.name)
        if not logger.propagate or logger.parent is None:
            break
        logger = logger.parent
    return [br for br in branches if br["logger"] in ploggers]


def get_activated_consoles(
    pbranches: Collection[Branch], record: LogRecord
) -> list[RichConsole]:
    aconsoles: list[RichConsole] = []
    for br in pbranches:
        if record.levelno < br["handler"].level:
            continue
        match fltr := br.get("filter"):
            case None:
                a = True
            case FilterCallable() | FilterFilterable():
                a = filtlog(fltr, record)
            case Collection():
                a = all(filtlog(f, record) for f in fltr)
        if a:
            aconsoles.append(br["console"])
    return aconsoles
