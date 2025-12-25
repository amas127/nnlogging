import logging
from unittest.mock import Mock

import pytest

from nnlogging.utils import (
    attach_handler_logfilter,
    detach_handler_logfilter,
    get_logfilter,
)


class TestGetLogfilter:
    def test_get_logfilter_none(self):
        assert get_logfilter(None) is None

    def test_get_logfilter_str(self):
        name = "foo.baz"
        fltr = get_logfilter(name)
        assert isinstance(fltr, logging.Filter)
        assert fltr.name == name

    def test_get_logfilter_lfilter(self):
        fltr = logging.Filter("boo.baz")
        fltr_got = get_logfilter(fltr)
        assert isinstance(fltr_got, logging.Filter)
        assert fltr.name == fltr_got.name

    def test_get_logfilter_collection(self):
        collections = ["foo", logging.Filter("foo.baz"), "foo.baz.boo"]
        fltr_got = get_logfilter(collections)
        assert isinstance(fltr_got, list)
        assert all(isinstance(f, logging.Filter) for f in fltr_got)
        for f1, f2 in zip(collections, fltr_got, strict=True):
            match f1:
                case str():
                    assert f2.name == f1
                case logging.Filter():
                    assert f2.name == f1.name

    def test_get_logfilter_invalid(self):
        with pytest.raises(TypeError):
            get_logfilter(1)


@pytest.fixture
def mock_handler_nofltr():
    mock = logging.Handler()
    mock.emit = Mock()
    return mock


class TestAttachHandlerLogfilter:
    def test_attach_none(self, mock_handler_nofltr):
        attach_handler_logfilter(mock_handler_nofltr, None)
        assert mock_handler_nofltr.filters == []

    def test_attach_one(self, mock_handler_nofltr):
        fltr = get_logfilter("foo")
        attach_handler_logfilter(mock_handler_nofltr, fltr)
        assert mock_handler_nofltr.filters == [fltr]

    def test_attach_many(self, mock_handler_nofltr):
        fltr = get_logfilter(["foo", logging.Filter("bar")])
        attach_handler_logfilter(mock_handler_nofltr, fltr)
        assert mock_handler_nofltr.filters == fltr

    def test_attach_invalid(self, mock_handler_nofltr):
        with pytest.raises(TypeError):
            attach_handler_logfilter(mock_handler_nofltr, 1)


@pytest.fixture
def mock_handler_hasfltr():
    mock = logging.Handler()
    attach_handler_logfilter(mock, get_logfilter(["foo", "bar"]))
    mock.emit = Mock()
    return mock


class TestDetachHandlerLogfilter:
    def _comp_fltrs(self, f1s, f2s):
        for f1, f2 in zip(f1s, f2s):
            assert f1.name == f2.name

    def test_detach_none(self, mock_handler_hasfltr):
        detach_handler_logfilter(mock_handler_hasfltr, None)
        self._comp_fltrs(mock_handler_hasfltr.filters, get_logfilter(["foo", "bar"]))

    def test_detach_one(self, mock_handler_hasfltr):
        detach_handler_logfilter(mock_handler_hasfltr, mock_handler_hasfltr.filters[0])
        self._comp_fltrs(mock_handler_hasfltr.filters, get_logfilter(["bar"]))

    def test_detach_notin(self, mock_handler_hasfltr):
        detach_handler_logfilter(mock_handler_hasfltr, get_logfilter("notexist"))
        self._comp_fltrs(mock_handler_hasfltr.filters, get_logfilter(["foo", "bar"]))

    def test_detach_many(self, mock_handler_hasfltr):
        detach_handler_logfilter(mock_handler_hasfltr, mock_handler_hasfltr.filters)
        self._comp_fltrs(mock_handler_hasfltr.filters, [])

    def test_detach_invalide(self, mock_handler_hasfltr):
        with pytest.raises(TypeError):
            detach_handler_logfilter(mock_handler_hasfltr, 1)
