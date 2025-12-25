import logging
from typing import Any

import pytest

from nnlogging.typings import Branch
from nnlogging.utils._render import (
    get_activated_consoles,
    get_propagated_branches,
    mock_logrecord,
)


@pytest.fixture
def logger_tree():
    root = logging.getLogger("foo")
    parent = logging.getLogger("foo.parent")
    child = logging.getLogger("foo.parent.child")
    for l in (root, parent, child):
        l.setLevel(logging.DEBUG)
        l.propagate = True
    yield root, parent, child
    for l in (root, parent, child):
        l.setLevel(logging.NOTSET)


@pytest.fixture
def mock_handler():
    handler = logging.Handler()
    handler.setLevel(logging.DEBUG)
    return handler


@pytest.fixture
def mock_branch_factory():
    def create_branch(
        logger: logging.Logger,
        level: int = logging.DEBUG,
        filter: Any = None,
        console: Any = None,
    ) -> Branch:
        handler = logging.Handler()
        handler.level = level
        if console is None:
            console = object()
        return {
            "logger": logger.name,
            "handler": handler,
            "filter": filter,
            "console": console,
        }

    return create_branch


@pytest.fixture
def sample_record(logger_tree):
    root, parent, child = logger_tree
    return mock_logrecord(child, logging.INFO)


# Tests for mock_logrecord
def test_mock_logrecord_returns_logrecord(logger_tree):
    root, _, _ = logger_tree
    record = mock_logrecord(root, logging.INFO)
    assert isinstance(record, logging.LogRecord)


def test_mock_logrecord_correct_level(logger_tree):
    root, _, _ = logger_tree
    record = mock_logrecord(root, logging.WARNING)
    assert record.levelno == 30


@pytest.mark.parametrize(
    "level,expected",
    [
        (logging.DEBUG, 10),
        (logging.INFO, 20),
        (logging.ERROR, 40),
        (logging.CRITICAL, 50),
    ],
)
def test_mock_logrecord_with_different_levels(logger_tree, level, expected):
    root, _, _ = logger_tree
    record = mock_logrecord(root, level)
    assert record.levelno == expected


# Tests for get_propagated_branches
def test_empty_branches_returns_empty(logger_tree):
    _, _, child = logger_tree
    result = get_propagated_branches([], child, logging.INFO)
    assert result == []


def test_logger_disabled_for_level(logger_tree):
    root, parent, child = logger_tree
    child.setLevel(logging.ERROR)
    result = get_propagated_branches([], child, logging.INFO)
    assert result == []


def test_propagation_chain_matching(logger_tree, mock_branch_factory):
    root, parent, child = logger_tree
    branches = [
        mock_branch_factory(root),
        mock_branch_factory(parent),
        mock_branch_factory(child),
    ]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert len(result) == 3
    assert result[0]["logger"] == root.name
    assert result[1]["logger"] == parent.name
    assert result[2]["logger"] == child.name


def test_propagate_false_stops_chain(logger_tree, mock_branch_factory):
    root, parent, child = logger_tree
    parent.propagate = False
    branches = [
        mock_branch_factory(root),
        mock_branch_factory(parent),
        mock_branch_factory(child),
    ]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert len(result) == 2
    assert result[0]["logger"] == parent.name
    assert result[1]["logger"] == child.name


def test_root_logger_no_parent(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    branches = [mock_branch_factory(root)]
    result = get_propagated_branches(branches, root, logging.INFO)
    assert len(result) == 1
    assert result[0]["logger"] == root.name


def test_no_matching_loggers(mock_branch_factory):
    other_logger = logging.getLogger("other")
    branches = [mock_branch_factory(other_logger)]
    child = logging.getLogger("parent.child")
    result = get_propagated_branches(branches, child, logging.INFO)
    assert result == []


# Tests for get_activated_consoles
def test_empty_pbranches_returns_empty(sample_record):
    result = get_activated_consoles([], sample_record)
    assert result == []


def test_no_filters_returns_all(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    branches = [
        mock_branch_factory(child, level=logging.DEBUG, filter=None),
        mock_branch_factory(child, level=logging.DEBUG, filter=None),
    ]
    result = get_activated_consoles(branches, sample_record)
    assert len(result) == 2
    assert result[0] == branches[0]["console"]
    assert result[1] == branches[1]["console"]


def test_handler_level_filter(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    branch1 = mock_branch_factory(child, level=logging.WARNING, filter=None)
    branch2 = mock_branch_factory(child, level=logging.DEBUG, filter=None)
    result = get_activated_consoles([branch1, branch2], sample_record)
    assert len(result) == 1
    assert result[0] == branch2["console"]


def test_single_callable_filter_true(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree

    def filter_true(record):
        return True

    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filter_true)
    result = get_activated_consoles([branch], sample_record)
    assert len(result) == 1


def test_single_callable_filter_false(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree

    def filter_false(record):
        return False

    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filter_false)
    result = get_activated_consoles([branch], sample_record)
    assert result == []


def test_filter_filterable_instance(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree

    class MyFilter(logging.Filter):
        def filter(self, record):
            return True

    filter_obj = MyFilter()
    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filter_obj)
    result = get_activated_consoles([branch], sample_record)
    assert len(result) == 1
    # Test false

    class MyFilterFalse(logging.Filter):
        def filter(self, record):
            return False

    filter_false = MyFilterFalse()
    branch2 = mock_branch_factory(child, level=logging.DEBUG, filter=filter_false)
    result2 = get_activated_consoles([branch2], sample_record)
    assert result2 == []


def test_filter_collection_all_true(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree

    def f1(r):
        return True

    def f2(r):
        return True

    branch = mock_branch_factory(child, level=logging.DEBUG, filter=[f1, f2])
    result = get_activated_consoles([branch], sample_record)
    assert len(result) == 1


def test_filter_collection_one_false(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree

    def f1(r):
        return True

    def f2(r):
        return False

    branch = mock_branch_factory(child, level=logging.DEBUG, filter=[f1, f2])
    result = get_activated_consoles([branch], sample_record)
    assert result == []


def test_mixed_console_inclusion(sample_record, mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    branch1 = mock_branch_factory(child, level=logging.DEBUG, filter=None)
    branch2 = mock_branch_factory(child, level=logging.WARNING, filter=None)

    def f_false(r):
        return False

    branch3 = mock_branch_factory(child, level=logging.DEBUG, filter=f_false)
    result = get_activated_consoles([branch1, branch2, branch3], sample_record)
    assert len(result) == 1
    assert result[0] == branch1["console"]


def test_many_branches_per_logger(mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    branches = [mock_branch_factory(child) for _ in range(5)]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert len(result) == 5


def test_unicode_in_record_message(mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    record = mock_logrecord(child, logging.INFO)
    record.msg = "héllo wörld"

    def filter_check(r):
        return "héllo" in r.msg

    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filter_check)
    result = get_activated_consoles([branch], record)
    assert len(result) == 1


def test_mock_logrecord_attributes(logger_tree):
    root, _, _ = logger_tree
    record = mock_logrecord(root, logging.INFO)
    assert record.name == root.name
    assert record.levelno == logging.INFO


def test_get_propagated_branches_effective_level(logger_tree, mock_branch_factory):
    root, parent, child = logger_tree
    child.setLevel(logging.INFO)
    branches = [
        mock_branch_factory(root),
        mock_branch_factory(parent),
        mock_branch_factory(child),
    ]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert all(l1.name == l2["logger"] for l1, l2 in zip(logger_tree, result))


def test_get_propagated_branches_not_effective_level(logger_tree, mock_branch_factory):
    root, parent, child = logger_tree
    child.setLevel(logging.ERROR)
    branches = [
        mock_branch_factory(root),
        mock_branch_factory(parent),
        mock_branch_factory(child),
    ]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert result == []


def test_get_activated_consoles_level_equal(
    sample_record, mock_branch_factory, logger_tree
):
    _, _, child = logger_tree
    branch = mock_branch_factory(child, level=logging.INFO, filter=None)
    result = get_activated_consoles([branch], sample_record)
    assert len(result) == 1


def test_get_activated_consoles_collection_filterables(
    sample_record, mock_branch_factory, logger_tree
):
    _, _, child = logger_tree

    class MyFilter(logging.Filter):
        def filter(self, record):
            return True

    filters = [MyFilter(), MyFilter()]
    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filters)
    result = get_activated_consoles([branch], sample_record)
    assert len(result) == 1


def test_get_activated_consoles_invalid_single_filter(
    sample_record, mock_branch_factory, logger_tree
):
    _, _, child = logger_tree
    branch = mock_branch_factory(child, level=logging.DEBUG, filter="invalid")
    with pytest.raises(TypeError):
        get_activated_consoles([branch], sample_record)


def test_get_activated_consoles_collection_with_invalid(
    sample_record, mock_branch_factory, logger_tree
):
    _, _, child = logger_tree
    filters = [lambda r: True, "invalid"]
    branch = mock_branch_factory(child, level=logging.DEBUG, filter=filters)
    with pytest.raises(TypeError):
        get_activated_consoles([branch], sample_record)


def test_scalability_1000_branches(mock_branch_factory, logger_tree):
    _, _, child = logger_tree
    branches = [mock_branch_factory(child) for _ in range(1000)]
    result = get_propagated_branches(branches, child, logging.INFO)
    assert len(result) == 1000


def test_deep_propagation_chain(mock_branch_factory):
    # Create a deep chain
    loggers = []
    for i in range(10):
        name = ".".join([f"level{j}" for j in range(i + 1)])
        loggers.append(logging.getLogger(name))
    for l in loggers:
        l.setLevel(logging.DEBUG)
    branches = [mock_branch_factory(l) for l in loggers]
    result = get_propagated_branches(branches, loggers[-1], logging.INFO)
    assert len(result) == 10
    # Cleanup
    for l in loggers:
        l.setLevel(logging.NOTSET)
