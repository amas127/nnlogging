from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from logging import (
    Filter as _Filter,
    Formatter as _Formatter,
    LogRecord as _LogRecord,
    Logger as _Logger,
)
from typing import TypeAlias
from warnings import WarningMessage as _WarnMsg

from ._rich import RichText


Logger: TypeAlias = _Logger
LogTimeFormatter: TypeAlias = Callable[[datetime], str | RichText]
Level: TypeAlias = int | str
LogMsgFormatter: TypeAlias = _Formatter
LogFilter: TypeAlias = str | _Filter
LogRecord: TypeAlias = _LogRecord
WarnMsg: TypeAlias = _WarnMsg
