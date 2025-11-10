import sys
from io import StringIO

import pytest
from rich.emoji import Emoji
from rich.highlighter import (
    NullHighlighter as RichNullHighlighter,
    ReprHighlighter as RichReprHighlighter,
)
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree


@pytest.fixture(params=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "int"])
def logger_level(request, log_level_int_gen):
    match request.param:
        case str() if request.param != "int":
            return request.param
        case "int":
            return log_level_int_gen()
        case _:
            raise RuntimeError


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


@pytest.fixture(params=[None, "auto", "standard", "truecolor"])
def branch_color_system(request):
    return request.param


@pytest.fixture(params=["stderr", "stdout"])
def global_shell_sink(request):
    return getattr(sys, request.param)


@pytest.fixture
def global_shell_name(shell_name_gen):
    return shell_name_gen()


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
