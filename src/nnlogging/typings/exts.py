import sys

if sys.version_info >= (3, 11):
    from typing import Never, NotRequired, Required, Unpack
else:
    from typing_extensions import Never, NotRequired, Required, Unpack


__all__ = [
    # py311
    "NotRequired",
    "Required",
    "Unpack",
    "Never",
]
