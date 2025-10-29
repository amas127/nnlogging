from dataclasses import make_dataclass
from datetime import datetime
from io import StringIO
from logging import Formatter
from sys import stderr

import pytest
from rich.highlighter import NullHighlighter, ReprHighlighter
from rich.text import Text

from nnlogging.utils import (
    LoggerConfig,
    RunConfig,
    get_rich_console,
    get_rich_progress_default_columns,
)

# ====== helper ====== #


@pytest.fixture(
    params=(
        (None, None),
        (..., ...),
        (None, ...),
        (..., None),
    )
)
def or_example(request):
    return request.param


@pytest.fixture(params=(True, False))
def evolve_match(request):
    return request.param


@pytest.fixture
def evolve_example(
    evolve_match,
    dataclass_name_gen,
    dataclass_key_gen,
    dataclass_value_gen,
):
    dataclass_name = dataclass_name_gen()
    dataclass_key = dataclass_key_gen()
    cls = make_dataclass(dataclass_name, ((dataclass_key, str, dataclass_value_gen()),))
    if evolve_match:
        return evolve_match, cls, dataclass_key
    else:
        return evolve_match, cls, "CANNOTMATCH"


# ====== rich factory ====== #


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


@pytest.fixture(params=["repr", None, "null"])
def console_highlighter(request):
    match request.param:
        case "repr":
            return ReprHighlighter()
        case "null":
            return NullHighlighter()
        case None:
            return None
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


@pytest.fixture(params=["repr", None, "null"])
def handler_highlighter(request):
    match request.param:
        case "repr":
            return ReprHighlighter()
        case "null":
            return NullHighlighter()
        case None:
            return None
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


@pytest.fixture(params=[None, "default"])
def progress_columns(request):
    match request.param:
        case None:
            return None
        case "default":
            return get_rich_progress_default_columns()
        case _:
            raise RuntimeError


# ====== branch factory ====== #


# ------ logger ------ #
@pytest.fixture
def logger_name(logger_name_gen):
    return logger_name_gen()


@pytest.fixture(params=["random", Ellipsis])
def logger_name_omitable(request, logger_name_gen):
    match request.param:
        case "random":
            return logger_name_gen()
        case _ if request.param is ...:
            return request.param
        case _:
            raise RuntimeError


@pytest.fixture(params=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "int"])
def logger_level(request, log_level_int_gen):
    match request.param:
        case str() if request.param != "int":
            return request.param
        case "int":
            return log_level_int_gen()
        case _:
            raise RuntimeError


@pytest.fixture(params=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "int", Ellipsis])
def logger_level_omitable(request, log_level_int_gen):
    match request.param:
        case str() if request.param != "int":
            return request.param
        case "int":
            return log_level_int_gen()
        case _ if request.param is ...:
            return request.param
        case _:
            raise RuntimeError


@pytest.fixture(params=[True, False])
def logger_propagate(request):
    return request.param


@pytest.fixture(params=[True, False, Ellipsis])
def logger_propagate_omitable(request):
    return request.param


@pytest.fixture(params=[None, "random"])
def logger_config(
    request,
    logger_name,
    logger_level,
    logger_propagate,
):
    match request.param:
        case None:
            return None
        case "random":
            return LoggerConfig(
                name=logger_name,
                level=logger_level,
                propagate=logger_propagate,
            )
        case _:
            raise RuntimeError


@pytest.fixture(params=[Ellipsis, "random"])
def run_experiment_omitable(request, experiment_name_gen):
    match request.param:
        case "random":
            return experiment_name_gen()
        case _ if request.param is Ellipsis:
            return Ellipsis
        case _:
            raise RuntimeError


@pytest.fixture
def run_experiment(experiment_name_gen):
    return experiment_name_gen()


@pytest.fixture(params=[None, "random"])
def run_config(
    request,
    run_experiment,
    root_path,
):
    match request.param:
        case None:
            return None
        case "random":
            return RunConfig(
                experiment=run_experiment,
                repo=str(root_path),
            )
        case _:
            raise RuntimeError
