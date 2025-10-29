import pytest

from nnlogging.utils import evolve_, or_


def test_or_(or_example):
    value, default = or_example
    returned = or_(value, default)
    targeted = default if isinstance(value, type(...)) else value
    assert returned == targeted


def test_evolve_(
    evolve_example,
    dataclass_value_gen,
):
    match_, cls, k = evolve_example
    if match_:
        v = dataclass_value_gen()
        inst = evolve_(cls(), **{k: v})
        assert getattr(inst, k) == v
    else:
        with pytest.raises(Exception):
            evolve_(cls(), **{k: dataclass_value_gen()})
