import logging
import sys
from io import StringIO
from unittest.mock import Mock

import pytest

from nnlogging.helpers import now
from nnlogging.options import (
    ConsoleFullOpt,
    HandlerFullOpt,
    HandlerSetupFullOpt,
    ProgressFullOpt,
    ProgressSetupFullOpt,
    TaskFullOpt,
)
from nnlogging.typings import LogMsgFormatter, RichConsole, RichHandler, RichProgress
from nnlogging.utils import get_rconsole, get_rhandler, get_rprogress, get_rtask


@pytest.fixture
def mock_console():
    console = Mock(spec=RichConsole)
    console.get_time = lambda: now().isoformat()
    return console


@pytest.fixture
def mock_progress():
    mock = Mock(spec=RichProgress)
    mock.add_task.return_value = 0
    return mock


class TestGetRichConsole:
    def test_get_rconsole_default(self):
        console = get_rconsole("stderr", ConsoleFullOpt())
        assert isinstance(console, RichConsole)
        assert console.file == sys.stderr  # Default sink
        # Assert other defaults match
        assert console._width is None
        assert console._height is None
        assert console._markup is True
        assert console._emoji is True

    @pytest.mark.parametrize(
        "sink", ["stderr", "stdout", sys.stderr, sys.stdout, StringIO()]
    )
    def test_get_rconsole_sink(self, sink):
        console = get_rconsole(sink, ConsoleFullOpt())
        assert isinstance(console, RichConsole)
        expected_sink = getattr(sys, sink) if isinstance(sink, str) else sink
        assert console.file == expected_sink

    @pytest.mark.parametrize("width", [120, None])
    @pytest.mark.parametrize("height", [10, None])
    @pytest.mark.parametrize("emoji", [True, False])
    @pytest.mark.parametrize("soft_wrap", [True, False])
    def test_get_rconsole_kwargs(self, width, height, emoji, soft_wrap):
        console = get_rconsole(
            "stderr",
            ConsoleFullOpt(
                width=width, height=height, emoji=emoji, soft_wrap=soft_wrap
            ),
        )
        assert console._width == width
        assert console._height == height
        assert console._emoji == emoji
        assert console.soft_wrap == soft_wrap


class TestGetRichHandler:
    def test_get_rhandler_with_console(self, mock_console):
        handler = get_rhandler(mock_console, HandlerFullOpt())
        assert isinstance(handler, RichHandler)

    def test_get_rhandler_with_str_format(self, mock_console):
        handler = get_rhandler(
            mock_console, HandlerFullOpt(msgfmt="[%(level)s] {%(message)s}")
        )
        assert isinstance(handler.formatter, LogMsgFormatter)
        assert str(handler.formatter._fmt) == "[%(level)s] {%(message)s}"

    def test_get_rhandler_with_formatter_instance(self, mock_console):
        formatter = LogMsgFormatter("%(levelname)s: %(message)s")
        handler = get_rhandler(mock_console, HandlerFullOpt(msgfmt=formatter))
        assert handler.formatter is formatter

    @pytest.mark.parametrize("level", [logging.DEBUG, logging.INFO])
    @pytest.mark.parametrize("show_path", [True, False])
    def test_get_rhandler_parametrized(self, mock_console, level, show_path):
        handler = get_rhandler(
            mock_console,
            HandlerFullOpt(setup=HandlerSetupFullOpt(level=level, show_path=show_path)),
        )
        assert handler.level == level
        assert handler._log_render.show_path == show_path


class TestGetRichProgress:
    def test_get_rprogress_default(self, mock_console):
        progress = get_rprogress(mock_console, ProgressFullOpt())
        assert isinstance(progress, RichProgress)
        assert len(progress.columns) == 5
        assert progress.live.transient is False

    @pytest.mark.parametrize("transient", [True, False])
    @pytest.mark.parametrize("refresh_per_second", [5.0, 20.0])
    def test_get_rprogress_parametrized(
        self, mock_console, transient, refresh_per_second
    ):
        progress = get_rprogress(
            mock_console,
            ProgressFullOpt(
                setup=ProgressSetupFullOpt(
                    transient=transient, refresh_per_second=refresh_per_second
                )
            ),
        )
        assert progress.live.transient == transient
        assert progress.live.refresh_per_second == refresh_per_second

    def test_get_rprogress_custom_columns(self, mock_console):
        progress = get_rprogress(
            mock_console, ProgressFullOpt(columns=["col1", "col2"])
        )
        assert len(progress.columns) == 2


class TestGetRichTask:
    @pytest.mark.parametrize("total", [None, 10])
    def test_get_rtask_default(self, mock_console, total):
        progress = get_rprogress(mock_console, ProgressFullOpt())
        taskid = get_rtask(
            progress, TaskFullOpt(total=total, description="", completed=0.5)
        )
        assert isinstance(taskid, int)
