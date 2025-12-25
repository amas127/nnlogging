from __future__ import annotations

import sys
from os import PathLike
from types import TracebackType
from typing import TypeAlias, TypeGuard


if sys.version_info >= (3, 11):  # pragma: no cover
    from typing import Never, NotRequired, Required, Self, TypeVarTuple, Unpack
else:  # pragma: no cover
    from typing_extensions import (
        Never,
        NotRequired,
        Required,
        Self,
        TypeVarTuple,
        Unpack,
    )


if sys.version_info >= (3, 12):  # pragma: no cover
    from typing import override
else:  # pragma: no cover
    from typing_extensions import override

StrPath: TypeAlias = str | PathLike[str]
ExcInfoType: TypeAlias = (
    bool
    | BaseException
    | tuple[None, None, None]
    | tuple[type[BaseException], BaseException, TracebackType | None]
    | None
)

__all__ = [
    "ExcInfoType",
    "Never",
    "NotRequired",
    "Required",
    "Self",
    "StrPath",
    "TypeGuard",
    "TypeVarTuple",
    "Unpack",
    "override",
]
