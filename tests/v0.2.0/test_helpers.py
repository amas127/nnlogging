import logging
import math
from dataclasses import dataclass
from datetime import datetime

import pytest
from faker import Faker

from nnlogging.exceptions import (
    LevelNameNotFoundError,
    LevelTypeWeirdError,
    StacklevelTypeWeirdError,
)
from nnlogging.helpers import (
    asdict,
    compose,
    dumps,
    get_level,
    inc_stacklevel,
    inj_excinfo,
    loads,
)


fake = Faker()


@pytest.fixture
def random_text():
    def gen(maxchs: int):
        return fake.pystr(max_chars=maxchs)

    return gen


@pytest.fixture
def now():
    return datetime.now()


@dataclass(slots=True)
class MockSlotsDataclass:
    stacklevel: int = 1
    exc_info: bool | None = None


@dataclass
class MockDataclass:
    stacklevel: int = 1
    exc_info: bool | None = None
    name: str = "test"


@dataclass
class MockEmptyDataclass:
    pass


class TestGetLevel:
    @pytest.mark.parametrize(
        "lvl",
        [
            ("debug", 10),
            ("info", 20),
            ("warning", 30),
            ("error", 40),
            ("critical", 50),
            ("custom_get_level_str", 42),
        ],
    )
    def test_get_level_str(self, lvl):
        lvlstr, lvlint = lvl
        logging.addLevelName(42, "CUSTOM_GET_LEVEL_STR")
        assert get_level(lvlstr) == lvlint

    @pytest.mark.parametrize("lvl", [42, 0, 1024])
    def test_get_level_int(self, lvl):
        assert lvl == get_level(lvl)

    def test_get_level_nostr(self):
        with pytest.raises(LevelNameNotFoundError):
            get_level("weird_get_level_str")

    def test_get_level_weirdtype(self):
        with pytest.raises(LevelTypeWeirdError):
            get_level(type("Weird", (), {}))


class TestIncStacklevel:
    def test_inc_stacklevel_nostacklevel(self):
        assert inc_stacklevel({}) == {}

    def test_inc_stacklevel_default(self):
        assert inc_stacklevel({"stacklevel": 42}, inc=2) == {"stacklevel": 44}

    def test_inc_stacklevel_notint(self):
        with pytest.raises(StacklevelTypeWeirdError):
            inc_stacklevel({"stacklevel": 4.2})

    def test_inc_stacklevel_dataclass(self):
        obj = MockDataclass(stacklevel=10)
        inc_stacklevel(obj, inc=2)
        assert obj.stacklevel == 12

    def test_inc_stacklevel_non_target(self):
        assert inc_stacklevel(123) == 123
        assert inc_stacklevel("foo") == "foo"

    def test_inc_stacklevel_has_target(self):
        assert inc_stacklevel({"stacklevel": 1}, inc=2) == {"stacklevel": 3}

    def test_inc_stacklevel_dataclass_no_attr(self):
        obj = MockEmptyDataclass()
        assert inc_stacklevel(obj) == obj


class TestInjExcinfo:
    def test_inj_excinfo_dict(self):
        d = {}
        inj_excinfo(d, exc=True)
        assert d["exc_info"] is True

        d = {"exc_info": None}
        inj_excinfo(d, exc=True)
        assert d["exc_info"] is True

        d = {"exc_info": False}
        inj_excinfo(d, exc=True)
        assert d["exc_info"] is False

    def test_inj_excinfo_dataclass(self):
        obj = MockDataclass(exc_info=None)
        inj_excinfo(obj, exc=True)
        assert obj.exc_info is True

        obj = MockDataclass(exc_info=False)
        inj_excinfo(obj, exc=True)
        assert obj.exc_info is False  # Due to 'or' logic in implementation

    def test_inj_excinfo_non_target(self):
        assert inj_excinfo(123) == 123
        assert inj_excinfo("foo") == "foo"

    def test_inj_excinfo_has_target(self):
        assert inj_excinfo({"exc_info": None}) == {"exc_info": True}
        exc = ZeroDivisionError()
        assert inj_excinfo({"exc_info": None}, exc=exc) == {"exc_info": exc}

    def test_inj_excinfo_dataclass_no_attr(self):
        obj = MockEmptyDataclass()
        assert inj_excinfo(obj) is obj


class TestAsDict:
    def test_asdict_regular(self):
        obj = MockDataclass(name="foo")
        d = asdict(obj)
        assert d["name"] == "foo"
        assert "stacklevel" in d

    def test_asdict_slots(self):
        obj = MockSlotsDataclass(stacklevel=5)
        d = asdict(obj)
        assert d["stacklevel"] == 5


class TestCompose:
    def test_compose_single_function(self):
        inc = lambda x: x + 1
        composed = compose(inc)
        assert composed(5) == 6

    def test_compose_two_functions(self):
        double = lambda x: x * 2
        inc = lambda x: x + 1
        composed = compose(double, inc)
        assert composed(3) == 8

    def test_compose_three_functions(self):
        square = lambda x: x**2
        inc = lambda x: x + 1
        double = lambda x: x * 2
        composed = compose(double, inc, square)
        assert composed(3) == 20

    def test_compose_function_returning_none(self):
        f1 = lambda x: None
        f2 = lambda x: x * 2 if x is not None else 0
        composed = compose(f2, f1)
        assert composed(5) == 0

    def test_compose_function_returning_string(self):
        to_str = lambda x: str(x)
        upper = lambda s: s.upper()
        composed = compose(upper, to_str)
        assert composed(123) == "123".upper() == "123"

    def test_compose_builtin_functions(self):
        abs_func = abs
        square = lambda x: x**2
        composed = compose(square, abs_func)
        assert composed(-3) == 9

    def test_compose_no_funcs_empty(self):
        assert compose()() is None

    def test_compose_no_funcs_1(self):
        assert compose()(1) == 1

    def test_compose_no_funcs_tuple(self):
        assert compose()(1, 2) == (1, 2)

    @pytest.mark.parametrize(
        "everything",
        [
            ((lambda x: x + 1,), 1, 2),
            ((lambda x: x * 2, lambda x: x), 5, 10),
            ((lambda x: -x, lambda x: x**2, lambda x: x + 1), 3, -16),
        ],
    )
    def test_compose_funcs(self, everything):
        fs, i, o = everything
        assert compose(*fs)(i) == o

    def test_multiple_arguments(self):
        with pytest.raises(TypeError):
            compose(lambda x: x + 1)(1, 2)

    def test_function_with_kwargs(self):
        with pytest.raises(TypeError):
            compose(lambda a, b: a + b)(1)

    def test_compose_func_returns_tuple(self):
        f1 = lambda x: (x, x + 1)
        f2 = lambda x, y: x + y
        composed = compose(f2, f1)
        assert composed(5) == 11


class TestLoads:
    def test_loads_str(self):
        x = dumps({"4": 5})
        y = {"4": 5}
        assert loads(x) == y

    def test_loads_list(self):
        x = [dumps(4), dumps([4, 5]), dumps({"4": 5})]
        y = [4, [4, 5], {"4": 5}]
        assert loads(x) == y

    def test_loads_dict(self):
        x = {"4": dumps([4, 5])}
        y = {"4": [4, 5]}
        assert loads(x) == y

    def test_loads_pyobj(self):
        x = y = 1
        assert loads(x) == y

    def test_loads_bytes(self):
        assert loads(b'{"a": 1}') == {"a": 1}

    def test_loads_bytearray(self):
        assert loads(bytearray(b'{"a": 1}')) == {"a": 1}

    def test_loads_memoryview(self):
        assert loads(memoryview(b'{"a": 1}')) == {"a": 1}

    def test_loads_tuple(self):
        assert loads((b"1", b"2")) == (1, 2)


class TestDumps:
    def test_dumps_none(self):
        assert dumps(None) is None

    def test_dumps_dict(self):
        assert dumps({"a": 1}) == '{"a":1}'

    def test_dumps_empty_dict(self):
        assert dumps({}) == "{}"

    def test_dumps_list(self):
        assert dumps([1, 2, 3]) == "[1,2,3]"

    def test_dumps_string(self):
        assert dumps("hello") == '"hello"'

    def test_dumps_int_float(self):
        assert dumps(42) == "42"
        assert dumps(math.pi) == str(math.pi)

    def test_dumps_bool(self):
        assert dumps(True) == "true"
        assert dumps(False) == "false"

    def test_dumps_nested_dict(self):
        assert dumps({"a": [1, 2]}) == '{"a":[1,2]}'
