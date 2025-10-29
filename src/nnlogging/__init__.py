"""
Package: `nnlogging`
Version: ``0.1.1``
"""

from .shell import Shell
from .utils import LoggerConfig

__all__ = ["Shell"]

shell = Shell(
    "__nnlogging__",
    logger_config=LoggerConfig(
        name="__nnlogging__",
    ),
)
