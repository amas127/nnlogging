import logging
from logging import Formatter

from rich.highlighter import NullHighlighter

from nnlogging.utils.factories import (
    get_aim_run,
    get_branch,
    get_logging_logger,
    get_rich_console,
    get_rich_handler,
    get_rich_progress,
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
            assert type(console.highlighter) is type(console_highlighter)


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
    assert type(handler.highlighter) is type(handler_highlighter)
    match handler_message_format:
        case str():
            assert handler.formatter is not None
            assert handler.formatter._fmt == handler_message_format
        case Formatter():
            assert handler.formatter._fmt is handler_message_format._fmt
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
    assert all(
        type(col_src) is type(col_tgt)
        for col_src, col_tgt in zip(progress_columns, progress.columns, strict=True)
    )


def test_get_logging_logger(
    logger_name,
    logger_level,
    logger_propagate,
):
    logger = get_logging_logger(
        name=logger_name,
        level=logger_level,
        propagate=logger_propagate,
    )
    assert logger.name == logger_name
    match logger_level:
        case str():
            assert logger.level == getattr(logging, logger_level)
        case int():
            assert logger.level == logger_level
        case _:
            raise RuntimeError
    assert logger.propagate == logger_propagate


def test_get_aim_run(
    root_path,
    run_experiment,
):
    run = get_aim_run(
        experiment=run_experiment,
        repo=str(root_path),
    )
    assert run.repo.path == str(root_path / ".aim")
    assert run.experiment == run_experiment or "default"


def test_get_branch(
    console_color_and_sink,
    console_width_and_height,
    console_highlighter,
    handler_level,
    handler_time_format,
    handler_message_format,
):
    color_system, sink = console_color_and_sink
    width, height = console_width_and_height
    branch = get_branch(
        sink,
        width=width,
        height=height,
        color_system=color_system,
        highlighter=console_highlighter,
        level=handler_level,
        log_time_format=handler_time_format,
        log_message_format=handler_message_format,
    )

    console = branch["console"]
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
            assert type(console.highlighter) is type(console_highlighter)

    handler = branch["handler"]
    assert handler.console is console
    match handler_level:
        case str():
            assert handler.level == getattr(logging, handler_level)
        case int():
            assert handler.level == handler_level
        case _:
            raise RuntimeError
    assert handler._log_render.time_format is handler_time_format
    assert type(handler.highlighter) is type(console_highlighter)
    match handler_message_format:
        case str():
            assert handler.formatter is not None
            assert handler.formatter._fmt == handler_message_format
        case Formatter():
            assert handler.formatter._fmt is handler_message_format._fmt
        case _:
            raise RuntimeError

    assert branch["tasks"] == dict()
    assert branch["progress"] is None
