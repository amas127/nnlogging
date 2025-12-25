from __future__ import annotations

import linecache
import logging
from functools import partial

from nnlogging.helpers import compose
from nnlogging.typings import WarnCapturer, WarnMsg


def default_warning_capturer() -> WarnCapturer:  # pragma: no cover
    def _formatter(wmsg: WarnMsg, /) -> str:
        s = f"{wmsg.category.__name__}: {wmsg.message}\n"
        if (
            line := linecache.getline(wmsg.filename, wmsg.lineno)
            if wmsg.line is None
            else wmsg.line
        ):
            s += f"> {line.strip()}\n"

        return s

    callback = partial(logging.getLogger("py.warnings").warning, stacklevel=3)
    return compose(callback, _formatter, WarnMsg)
