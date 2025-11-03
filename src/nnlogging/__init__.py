"""
Package: `nnlogging`
Version: ``0.1.1``
"""

from .shell import (
    Shell,
    get_global_shell,
    replace_global_shell,
)

__all__ = [
    "Shell",
    "get_global_shell",
    "replace_global_shell",
]
