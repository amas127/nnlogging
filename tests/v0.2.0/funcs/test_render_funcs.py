import logging
from unittest.mock import MagicMock

import pytest

from nnlogging.funcs import render
from nnlogging.options import RenderFullOpt


@pytest.fixture
def logger_tree():
    """Provides a root -> parent -> child logger hierarchy."""
    root = logging.getLogger("test_render")
    parent = logging.getLogger("test_render.parent")
    child = logging.getLogger("test_render.parent.child")
    for l in (root, parent, child):
        l.setLevel(logging.DEBUG)
        l.propagate = True
    yield root, parent, child
    # Cleanup
    for l in (root, parent, child):
        l.setLevel(logging.NOTSET)


@pytest.fixture
def mock_branch_factory():
    """Creates a mock branch dictionary compatible with nnlogging.typings.Branch."""

    def create_branch(
        logger: logging.Logger,
        level: int = logging.DEBUG,
        filter: any = None,
        console: MagicMock = None,
    ):
        handler = logging.Handler()
        handler.level = level
        if console is None:
            console = MagicMock()
        return {
            "logger": logger.name,
            "handler": handler,
            "filter": filter,
            "console": console,
        }

    return create_branch


def test_render_single_console(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    mock_console = MagicMock()
    branch = mock_branch_factory(root, console=mock_console)
    branches = {root.name: branch}
    opts = RenderFullOpt()

    render(branches, root, logging.INFO, "hello", kwargs=opts)

    mock_console.print.assert_called_once()
    args, _ = mock_console.print.call_args
    assert args == ("hello",)


def test_render_multiple_consoles(logger_tree, mock_branch_factory):
    root, parent, child = logger_tree
    c1, c2, c3 = MagicMock(), MagicMock(), MagicMock()
    branches = {
        root.name: mock_branch_factory(root, console=c1),
        parent.name: mock_branch_factory(parent, console=c2),
        child.name: mock_branch_factory(child, console=c3),
    }
    opts = RenderFullOpt()

    # Rendering at child should propagate to parent and root
    render(branches, child, logging.INFO, "hello", kwargs=opts)

    c1.print.assert_called_once()
    c2.print.assert_called_once()
    c3.print.assert_called_once()


def test_render_no_activated_consoles(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    mock_console = MagicMock()
    # Branch level (ERROR) is higher than render level (INFO)
    branch = mock_branch_factory(root, level=logging.ERROR, console=mock_console)
    branches = {root.name: branch}
    opts = RenderFullOpt()

    render(branches, root, logging.INFO, "hello", kwargs=opts)

    mock_console.print.assert_not_called()


def test_render_disabled_logger(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    root.setLevel(logging.ERROR)
    mock_console = MagicMock()
    branch = mock_branch_factory(root, level=logging.DEBUG, console=mock_console)
    branches = {root.name: branch}
    opts = RenderFullOpt()

    # Logger itself is disabled for INFO, so it shouldn't even check branches
    render(branches, root, logging.INFO, "hello", kwargs=opts)

    mock_console.print.assert_not_called()


def test_render_with_options(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    mock_console = MagicMock()
    branch = mock_branch_factory(root, console=mock_console)
    branches = {root.name: branch}
    # Test that options are correctly passed through asdict
    opts = RenderFullOpt(style="bold red", justify="center", markup=True)

    render(branches, root, logging.INFO, "hello", kwargs=opts)

    mock_console.print.assert_called_once()
    _, kwargs = mock_console.print.call_args
    assert kwargs["style"] == "bold red"
    assert kwargs["justify"] == "center"
    assert kwargs["markup"] is True


def test_render_multiple_objects(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    mock_console = MagicMock()
    branch = mock_branch_factory(root, console=mock_console)
    branches = {root.name: branch}
    opts = RenderFullOpt()

    render(branches, root, logging.INFO, "hello", "world", 123, kwargs=opts)

    mock_console.print.assert_called_once()
    args, _ = mock_console.print.call_args
    assert args == ("hello", "world", 123)


def test_render_with_filter(logger_tree, mock_branch_factory):
    root, _, _ = logger_tree
    c1, c2 = MagicMock(), MagicMock()

    def filter_pass(record):
        return True

    def filter_fail(record):
        return False

    branches = {
        "pass": mock_branch_factory(root, console=c1, filter=filter_pass),
        "fail": mock_branch_factory(root, console=c2, filter=filter_fail),
    }
    opts = RenderFullOpt()

    render(branches, root, logging.INFO, "hello", kwargs=opts)

    c1.print.assert_called_once()
    c2.print.assert_not_called()
