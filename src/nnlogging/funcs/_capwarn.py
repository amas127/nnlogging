import logging
import warnings

from nnlogging.options import CapwarnFullOpt


__all__ = ["capture_warnings"]


def capture_warnings(kwargs: CapwarnFullOpt) -> None:  # pragma: no cover
    if (enabled := kwargs.enabled) is not None:
        logging.captureWarnings(enabled)
        if enabled:
            warnings.showwarning = kwargs.capturer
