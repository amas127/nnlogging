import logging
import random
import sys
from io import StringIO

import pytest
from rich.emoji import Emoji
from rich.highlighter import ReprHighlighter as RichReprHighlighter
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree

from nnlogging.utils import BranchConfig, LoggerConfig, RunConfig


@pytest.fixture
def log_level_str_gen():
    levels = (
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    )

    def gen():
        return random.choice(levels)

    return gen


@pytest.fixture
def log_level_int_gen():
    levels = tuple(i for i in range(logging.DEBUG, logging.CRITICAL + 1) if i % 10 != 0)

    def gen():
        return random.choice(levels)

    return gen


@pytest.fixture(params=["default", None])
def logger_config(request):
    match request.param:
        case "default":
            return LoggerConfig()
        case None:
            return None
        case _:
            raise RuntimeError


@pytest.fixture(params=["str", "int", "ellipsis"])
def logger_level_omitable(
    request,
    log_level_str_gen,
    log_level_int_gen,
):
    match request.param:
        case "str":
            return log_level_str_gen()
        case "int":
            return log_level_int_gen()
        case "ellipsis":
            return Ellipsis
        case _:
            raise RuntimeError


@pytest.fixture(params=["default", None])
def run_config(request):
    match request.param:
        case "default":
            return RunConfig()
        case None:
            return None
        case _:
            raise RuntimeError


@pytest.fixture(params=["random", None, "ellipsis"])
def run_experiment_omitable(request, experiment_name_gen):
    match request.param:
        case "random":
            return experiment_name_gen()
        case None:
            return None
        case "ellipsis":
            return Ellipsis
        case _:
            raise RuntimeError


@pytest.fixture(params=["default", None])
def branch_config(request):
    match request.param:
        case "default":
            return BranchConfig()
        case None:
            return None
        case _:
            raise RuntimeError


@pytest.fixture(params=["repr", None, "ellipsis"])
def branch_highlighter_omitable(request):
    match request.param:
        case "repr":
            return RichReprHighlighter()
        case None:
            return None
        case "ellipsis":
            return Ellipsis
        case _:
            raise RuntimeError


@pytest.fixture(params=[None, "auto", "standard", "truecolor", "ellipsis"])
def branch_color_system_omitable(request):
    match request.param:
        case "ellipsis":
            return Ellipsis
        case _:
            return request.param


@pytest.fixture
def branch_name(branch_name_gen):
    return branch_name_gen()


@pytest.fixture(params=[None, "stderr", "stdout", "file", "stringio"])
def branch_sink(request, file_path_gen):
    match request.param:
        case None:
            return None
        case "stderr" | "stdout":
            return getattr(sys, request.param)
        case "file":
            return file_path_gen().open("a")
        case "stringio":
            return StringIO()
        case _:
            raise RuntimeError


@pytest.fixture
def run_metadata_label(run_metadata_label_gen):
    return run_metadata_label_gen()


@pytest.fixture(params=["float", "str", "list", "dict"])
def run_metadata(request, run_metadata_float_gen, run_metadata_str_gen):
    match request.param:
        case "float":
            return run_metadata_float_gen()
        case "str":
            return run_metadata_str_gen()
        case "tuple":
            return [run_metadata_str_gen(), run_metadata_str_gen()]
        case "dict":
            return {
                run_metadata_str_gen(): run_metadata_float_gen(),
            }


@pytest.fixture
def run_tag(run_metadata_label_gen):
    return run_metadata_label_gen()


@pytest.fixture
def task_name(task_name_gen):
    return task_name_gen()


@pytest.fixture
def task_desc(task_desc_gen):
    return task_desc_gen()


@pytest.fixture
def task_total_limited(task_total_int_gen):
    return task_total_int_gen()


@pytest.fixture
def task_total_unlimited():
    return None


@pytest.fixture(params=["limited", "unlimited"])
def task_total_gen(
    request,
    task_total_limited,
    task_total_unlimited,
):
    def gen():
        match request.param:
            case "limited":
                return task_total_limited
            case "unlimited":
                return task_total_unlimited
            case _:
                raise RuntimeError

    return gen


@pytest.fixture
def task_total(task_total_gen):
    return task_total_gen()


@pytest.fixture
def task_done(task_done_gen):
    return task_done_gen()


@pytest.fixture
def advance(task_advance_gen):
    return task_advance_gen()


@pytest.fixture(params=[10, 20, 30, 40, 50, "random"])
def log_level(request, log_level_int_gen):
    match request.param:
        case "random":
            return log_level_int_gen()
        case int():
            return request.param
        case _:
            raise RuntimeError


@pytest.fixture
def log_msg(message_gen):
    return message_gen()


@pytest.fixture(
    params=[
        "text",
        "emoji",
        "tree",
        "panel",
        "rule",
        "markdown",
        "syntax",
    ]
)
def renderable(request):
    item = None
    match request.param:
        case "text":
            item = Text.assemble(("Hello", "bold magenta"), ", World!")
        case "emoji":
            item = Emoji("warning")
        case "tree":
            item = Tree("[red]Rich Tree")
            foo = item.add("[yellow]foo")
            item.add("[green]baz")
            foo.add("[orange]sta")
        case "panel":
            item = Panel.fit("PANEL")
        case "rule":
            item = Rule("Rule Section")
        case "markdown":
            item = Markdown("# Hello\nThis is **bold**.")
        case "syntax":
            item = Syntax(
                'def hello():\n    print("Hi")',
                "python",
                line_numbers=True,
            )
        case _:
            raise RuntimeError
    return item
