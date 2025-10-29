import logging
from logging import Formatter

from rich.highlighter import Highlighter, NullHighlighter

from nnlogging.utils import (
    get_rich_console,
    get_rich_handler,
    get_rich_progress,
    get_rich_progress_default_columns,
)


def test_get_rich_console(
    console_color_and_sink,
    console_width_and_height,
    console_highlighter,
):
    color_system, sink = console_color_and_sink
    width, height = console_width_and_height

    console = get_rich_console(
        sink,
        width=width,
        height=height,
        color_system=color_system,
        highlighter=console_highlighter,
    )

    assert console.file == sink
    assert console._width == width
    assert console._height == height
    match color_system:
        case "auto":
            assert console._color_system == console._detect_color_system()
        case _:
            assert console.color_system == color_system
    match console_highlighter:
        case None:
            assert type(console.highlighter) is NullHighlighter
        case _:
            assert console.highlighter is console_highlighter


def test_get_rich_handler(
    console,
    handler_level,
    handler_time_format,
    handler_highlighter,
    handler_message_format,
):
    handler = get_rich_handler(
        console,
        level=handler_level,
        log_time_format=handler_time_format,
        highlighter=handler_highlighter,
        log_message_format=handler_message_format,
    )
    assert handler.console is console
    match handler_level:
        case str():
            assert handler.level == getattr(logging, handler_level)
        case int():
            assert handler.level == handler_level
        case _:
            raise RuntimeError
    assert handler._log_render.time_format is handler_time_format
    match handler_highlighter:
        case None:
            assert type(handler.highlighter) is NullHighlighter
        case Highlighter():
            assert handler.highlighter is handler_highlighter
        case _:
            raise RuntimeError
    match handler_message_format:
        case str():
            assert handler.formatter is not None
            assert handler.formatter._fmt == handler_message_format
        case Formatter():
            assert handler.formatter is handler_message_format
        case _:
            raise RuntimeError


def test_get_rich_progress(
    console,
    progress_columns,
):
    progress = get_rich_progress(
        console,
        columns=progress_columns,
    )
    assert progress.console is console
    if progress_columns is None:
        columns = get_rich_progress_default_columns()
        assert all(
            type(col_src) is type(col_tgt)
            for col_src, col_tgt in zip(columns, progress.columns, strict=True)
        )
    else:
        assert all(
            col_src is col_tgt
            for col_src, col_tgt in zip(progress_columns, progress.columns, strict=True)
        )


# @pytest.fixture(params=["nnlogging", Ellipsis])
# def logger_name(request):
#     return request.param


# @pytest.fixture(params=["INFO", 20, Ellipsis])
# def logger_level(request):
#     return request.param


# @pytest.fixture(params=[True, Ellipsis])
# def logger_propagate(request):
#     return request.param


# def test_get_logger(
#     logger_name,
#     logger_level,
#     logger_propagate,
# ):
#     logger = get_logger(
#         name=logger_name,
#         level=logger_level,
#         propagate=logger_propagate,
#     )
#     new_logger_config = LoggerConfig()
#     assert logger.name == (or_(logger_name, new_logger_config.name) or "root")
#     logger_level_new = or_(logger_level, new_logger_config.level)
#     match logger_level_new:
#         case str():
#             assert logger.level == getattr(logging, logger_level_new)
#         case int():
#             assert logger.level == logger_level_new
#         case _:
#             raise TypeError
#     assert logger.propagate == or_(logger_propagate, new_logger_config.propagate)


# def test_get_run(random_experiment_name, root_path: Path):
#     repo = Repo(str(root_path))
#     run = get_run(
#         experiment=random_experiment_name,
#         repo=str(root_path),
#     )
#     new_run_config = RunConfig()
#     try:
#         assert run.read_only == new_run_config.read_only
#         assert run.experiment == random_experiment_name
#         assert run.repo.path == str(root_path / ".aim")
#         assert repo.run_exists(run.hash)
#         assert run.hash in repo.list_all_runs()
#         assert run.hash in repo.list_active_runs()
#         assert run.hash not in repo.list_corrupted_runs()
#     finally:
#         run.close()
#         repo.close()
#         run_hash = run.hash
#         del run, repo  # safer cleaning
#         remove_run_success = subprocess.run(
#             ["aim", "runs", "--repo", str(root_path), "rm", "--yes", run_hash],
#             capture_output=True,
#         )
#         assert remove_run_success


# @pytest.fixture(params=[BranchConfig(), None])
# def branch_config(request):
#     return request.param


# @pytest.fixture(params=[None, "standard-console", "plain-text"])
# def branch_sink_and_color(request, random_file_path: Path):
#     match request.param:
#         case None:
#             return None, Ellipsis
#         case "standard-console":
#             return stderr, "standard"
#         case "plain-text":
#             return random_file_path.open("a"), None


# @pytest.fixture(params=[None, ReprHighlighter(), Ellipsis])
# def branch_highlighter(request):
#     return request.param


# @pytest.fixture(params=["INFO", 20, Ellipsis])
# def branch_level(request):
#     return request.param


# @pytest.fixture(params=("%(time)s - %(message)s", Formatter("%(time)s - %(message)s"), Ellipsis))
# def branch_log_message_format(request):
#     return request.param


# def test_get_branch(
#     branch_config,
#     branch_sink_and_color,
#     branch_highlighter,
#     branch_level,
#     branch_log_message_format,
# ):
#     sink, color_system = branch_sink_and_color
#     # new_branch_config = BranchConfig()
#     branch = get_branch(
#         config=branch_config,
#         sink=sink,
#         color_system=color_system,
#         highlighter=branch_highlighter,
#         level=branch_level,
#         log_message_format=branch_log_message_format,
#     )
#     new_branch_config = branch_config or BranchConfig()
#     assert branch["console"].file == sink or stderr
#     assert branch["handler"].console is branch["console"]
#     assert branch["progress"] is None
#     assert branch["tasks"] == dict()

#     color_system = or_(color_system, new_branch_config.color_system)
#     match color_system:
#         case "auto":
#             assert branch["console"]._color_system == branch["console"]._detect_color_system()
#         case _:
#             assert branch["console"].color_system == color_system

#     highlighter = or_(branch_highlighter, new_branch_config.highlighter)
#     match highlighter:
#         case RichHighlighter():
#             assert type(branch["console"].highlighter) is type(highlighter)
#             assert type(branch["handler"].highlighter) is type(highlighter)
#         case None:
#             assert type(branch["console"].highlighter) is RichNullHighlighter
#             assert type(branch["handler"].highlighter) is RichNullHighlighter

#     level = or_(branch_level, new_branch_config.level)
#     match level:
#         case str():
#             assert branch["handler"].level == getattr(logging, level)
#         case int():
#             assert branch["handler"].level == level

#     message_format = or_(branch_log_message_format, new_branch_config.log_message_format)
#     assert branch["handler"].formatter is not None
#     match message_format:
#         case str():
#             assert branch["handler"].formatter._fmt == Formatter(message_format)._fmt
#         case Formatter():
#             assert branch["handler"].formatter._fmt == message_format._fmt
