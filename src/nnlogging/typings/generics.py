import sys
from dataclasses import Field
from os import PathLike
from types import EllipsisType
from typing import Any, ClassVar, Protocol, TypeVar

if sys.version_info >= (3, 12):
    from typing import TypeAliasType
else:
    from typing_extensions import TypeAliasType


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]  # pyright: ignore[reportExplicitAny]


T = TypeVar("T")
PathT = TypeVar("PathT", str, bytes)


Omitable = TypeAliasType("Omitable", T | EllipsisType, type_params=(T,))
DataclassT = TypeVar("DataclassT", bound=DataclassInstance)
Pathlike = TypeAliasType("Pathlike", PathT | PathLike[PathT], type_params=(PathT,))
