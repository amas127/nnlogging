from datetime import datetime
from io import StringIO
from logging import Formatter
from sys import stderr

import pytest
from rich.highlighter import (
    NullHighlighter as RichNullHighlighter,
    ReprHighlighter as RichReprHighlighter,
)
from rich.text import Text

from nnlogging.options.rich_progress import get_default_progress_columns
from nnlogging.utils.factories import get_rich_console


@pytest.fixture(
    params=[
        "truecolor-stringio",
        "standard-console",
        "auto-console",
        "plain-file",
        "auto-file",
    ]
)
def console_color_and_sink(
    request,
    file_path_gen,
):
    match request.param:
        case "truecolor-stringio":
            io_ = StringIO()
            try:
                yield "truecolor", io_
            finally:
                io_.close()
        case "standard-console":
            yield "standard", stderr
        case "auto-console":
            yield "auto", stderr
        case "plain-file":
            io_ = file_path_gen().open("a")
            try:
                yield None, io_
            finally:
                io_.close()
        case "auto-file":
            io_ = file_path_gen().open("a")
            try:
                yield "auto", io_
            finally:
                io_.close()
        case _:
            raise RuntimeError


@pytest.fixture(params=[(None, None), (88, 10)])
def console_width_and_height(request):
    return request.param


@pytest.fixture(params=["repr", "null"])
def console_highlighter(request):
    match request.param:
        case "repr":
            return RichReprHighlighter()
        case "null":
            return RichNullHighlighter()
        case _:
            raise RuntimeError


@pytest.fixture(
    params=[
        "auto-console",
        "plain-file",
        "truecolor-stringio",
    ]
)
def console(request, file_path_gen):
    match request.param:
        case "auto-console":
            yield get_rich_console(stderr, color_system="auto")
        case "plain-file":
            io_ = file_path_gen().open("a")
            try:
                yield get_rich_console(io_, color_system=None)
            finally:
                io_.close()
        case "truecolor-stringio":
            io_ = StringIO()
            try:
                yield get_rich_console(
                    io_, color_system="truecolor", force_terminal=True
                )
            finally:
                io_.close()
        case _:
            raise RuntimeError


@pytest.fixture(params=["str", "int"])
def handler_level(
    request,
    log_level_int_gen,
    log_level_str_gen,
):
    match request.param:
        case "int":
            return log_level_int_gen()
        case "str":
            return log_level_str_gen()
        case _:
            raise RuntimeError


@pytest.fixture(params=["str", "callable"])
def handler_time_format(request):
    match request.param:
        case "str":
            return "%x %X"
        case "callable":

            def fmt(d: datetime):
                return Text(d.strftime("%x %X"))

            return fmt
        case _:
            raise RuntimeError


@pytest.fixture(params=["repr", "null"])
def handler_highlighter(request):
    match request.param:
        case "repr":
            return RichReprHighlighter()
        case "null":
            return RichNullHighlighter()
        case _:
            raise RuntimeError


@pytest.fixture(params=["str", "formatter"])
def handler_message_format(request):
    match request.param:
        case "str":
            return "%(time)s - %(message)s"
        case "formatter":
            return Formatter("%(time)s - %(message)s")
        case _:
            raise RuntimeError


@pytest.fixture(params=["default"])
def progress_columns(request):
    match request.param:
        case "default":
            return get_default_progress_columns()
        case _:
            raise RuntimeError


@pytest.fixture
def logger_name(logger_name_gen):
    return logger_name_gen()


@pytest.fixture(params=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "int"])
def logger_level(request, log_level_int_gen):
    match request.param:
        case str() if request.param != "int":
            return request.param
        case "int":
            return log_level_int_gen()
        case _:
            raise RuntimeError


@pytest.fixture(params=[True, False])
def logger_propagate(request):
    return request.param


@pytest.fixture(params=["random", None])
def run_experiment(request, experiment_name_gen):
    match request.param:
        case "random":
            return experiment_name_gen()
        case None:
            return None
        case _:
            raise RuntimeError


@pytest.fixture(params=["repr", "null"])
def branch_highlighter(request):
    match request.param:
        case "repr":
            return RichReprHighlighter()
        case "null":
            return RichNullHighlighter()
        case _:
            raise RuntimeError
