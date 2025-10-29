from dataclasses import replace
from types import EllipsisType

from nnlogging.typings import DataclassT, Omitable, T


def or_(
    value: Omitable[T],
    default: T,
    /,
) -> T:
    return default if isinstance(value, EllipsisType) else value


def evolve_(
    inst: DataclassT,
    /,
    **kwargs: object,
) -> DataclassT:
    evolutions = {k: v for k, v in kwargs.items() if not isinstance(v, EllipsisType)}
    return replace(inst, **evolutions)


def get_name(
    inst: object,
    /,
):
    inst_name = getattr(inst, "name", str(inst))
    assert isinstance(inst_name, str)
    return inst_name


def get__debugging(
    inst: object,
    /,
):
    inst_debugging = getattr(inst, "_debugging", False)
    assert isinstance(inst_debugging, bool)
    return inst_debugging
