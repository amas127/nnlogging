import logging
from dataclasses import dataclass
from typing import Any

import pytest
from faker import Faker

from nnlogging.funcs._log import (
    critical,
    debug,
    error,
    exception,
    info,
    log,
    warning,
)
from nnlogging.helpers import asdict, inc_stacklevel
from nnlogging.options import LogFullOpt


fake = Faker()


@dataclass
class MockLogger:
    """Mock logger that records all calls to log method."""

    calls: list[dict[str, Any]] = None

    def __post_init__(self):
        if self.calls is None:
            self.calls = []

    def log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Record the call to log method."""
        self.calls.append(
            {"level": level, "msg": msg, "args": args, "kwargs": kwargs.copy()}
        )


class TestLogFunction:
    """Test the main log function that all other functions delegate to."""

    @pytest.fixture
    def mock_logger(self):
        return MockLogger()

    @pytest.mark.parametrize(
        "level,msg,args,kwargs",
        [
            (logging.DEBUG, "debug message", (), LogFullOpt()),
            (logging.INFO, "info message", ("arg1",), LogFullOpt()),
            (
                logging.WARNING,
                "warning message",
                ("arg1", "arg2"),
                LogFullOpt(extra={"key": "value"}),
            ),
            (logging.ERROR, "error message", (), LogFullOpt(stacklevel=3)),
            (
                logging.CRITICAL,
                "critical message",
                ("arg1", "arg2", "arg3"),
                LogFullOpt(exc_info=True),
            ),
        ],
    )
    def test_log_function_calls_logger_log(self, mock_logger, level, msg, args, kwargs):
        """Test that log function calls logger.log with correct parameters."""
        log(mock_logger, level, msg, *args, kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["level"] == level
        assert call["msg"] == msg
        assert call["args"] == args
        assert call["kwargs"] == asdict(kwargs)

    def test_log_function_with_empty_kwargs(self, mock_logger):
        """Test log function with empty kwargs."""
        log(mock_logger, logging.INFO, "test message", kwargs=LogFullOpt())

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["level"] == logging.INFO
        assert call["msg"] == "test message"
        assert call["args"] == ()
        assert call["kwargs"] == asdict(inc_stacklevel(LogFullOpt()))

    def test_log_function_with_many_args(self, mock_logger):
        """Test log function with many arguments."""
        args = tuple(f"arg{i}" for i in range(10))
        log(mock_logger, logging.DEBUG, "message", *args, kwargs=LogFullOpt())

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["args"] == args
        assert call["kwargs"] == asdict(inc_stacklevel(LogFullOpt()))


class TestLevelSpecificFunctions:
    """Test level-specific logging functions (debug, info, warning, error, critical)."""

    @pytest.fixture
    def mock_logger(self):
        return MockLogger()

    @pytest.mark.parametrize(
        "function,expected_level",
        [
            (debug, logging.DEBUG),
            (info, logging.INFO),
            (warning, logging.WARNING),
            (error, logging.ERROR),
            (critical, logging.CRITICAL),
        ],
    )
    def test_level_functions_call_log_with_correct_level(
        self, mock_logger, function, expected_level
    ):
        """Test that level-specific functions call log with the correct level."""
        function(mock_logger, "test message", kwargs=LogFullOpt())

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["level"] == expected_level
        assert call["msg"] == "test message"
        assert call["args"] == ()
        assert call["kwargs"] == asdict(inc_stacklevel(LogFullOpt(), inc=2))

    @pytest.mark.parametrize(
        "function,kwargs",
        [
            (debug, LogFullOpt),
            (info, LogFullOpt(stacklevel=2)),
            (warning, LogFullOpt(exc_info=True)),
            (error, LogFullOpt(stack_info=True)),
            (critical, LogFullOpt(extra={"key": "value"})),
            (debug, LogFullOpt(stacklevel=3, exc_info=False)),
            (info, LogFullOpt(stack_info=True, extra={"key": "value"})),
        ],
    )
    def test_level_functions_with_kwargs(self, mock_logger, function, kwargs):
        """Test level-specific functions with various kwargs."""
        function(mock_logger, "test message", kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["msg"] == "test message"
        assert call["args"] == ()
        assert call["kwargs"] == asdict(kwargs)

    @pytest.mark.parametrize(
        "function,args",
        [
            (debug, ()),
            (info, ("arg1",)),
            (warning, ("arg1", "arg2")),
            (error, ("arg1", "arg2", "arg3")),
            (critical, tuple(f"arg{i}" for i in range(10))),
        ],
    )
    def test_level_functions_with_args(self, mock_logger, function, args):
        """Test level-specific functions with various args."""
        kwargs = LogFullOpt()
        function(mock_logger, "test message", *args, kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["msg"] == "test message"
        assert call["args"] == args
        assert call["kwargs"] == asdict(kwargs)


class TestExceptionFunction:
    """Test the exception function specifically."""

    @pytest.fixture
    def mock_logger(self):
        return MockLogger()

    def test_exception_function_calls_log_with_error_level(self, mock_logger):
        """Test that exception function calls log with ERROR level."""
        kwargs = LogFullOpt()
        exception(mock_logger, "test exception", kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["level"] == logging.ERROR
        assert call["msg"] == "test exception"
        assert call["args"] == ()
        assert call["kwargs"] == asdict(kwargs)

    def test_exception_function_with_kwargs(self, mock_logger):
        """Test exception function with various kwargs."""
        kwargs = LogFullOpt(stacklevel=2, exc_info=False, extra={"k": "v"})
        exception(mock_logger, "test exception", kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["msg"] == "test exception"
        assert call["args"] == ()
        expected_kwargs = asdict(kwargs)
        assert call["kwargs"] == expected_kwargs

    def test_exception_function_with_args(self, mock_logger):
        """Test exception function with args."""
        args = ("arg1", "arg2", "arg3")
        kwargs = LogFullOpt()
        exception(mock_logger, "test exception", *args, kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["msg"] == "test exception"
        assert call["args"] == args
        assert call["kwargs"] == asdict(kwargs)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.fixture
    def mock_logger(self):
        return MockLogger()

    def test_no_arguments(self, mock_logger: MockLogger):
        debug(mock_logger, "debug", kwargs=LogFullOpt())
        info(mock_logger, "info", kwargs=LogFullOpt())
        warning(mock_logger, "warning", kwargs=LogFullOpt())
        error(mock_logger, "error", kwargs=LogFullOpt())
        critical(mock_logger, "critical", kwargs=LogFullOpt())
        exception(mock_logger, "exception", kwargs=LogFullOpt())

        assert len(mock_logger.calls) == 6

        expected_levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
            logging.ERROR,
        ]
        for i, (call, expected_level) in enumerate(
            zip(mock_logger.calls, expected_levels)
        ):
            assert call["level"] == expected_level
            assert (
                call["msg"]
                == ["debug", "info", "warning", "error", "critical", "exception"][i]
            )
            assert call["args"] == ()
            assert call["kwargs"] == asdict(
                LogFullOpt(
                    stacklevel=3, exc_info=True if call["msg"] == "exception" else None
                )
            )

    def test_mixed_kwargs(self, mock_logger: MockLogger):
        """Test logging functions with mixed kwargs."""
        kwargs = LogFullOpt(
            stacklevel=5,
            exc_info=True,
            stack_info=True,
            extra={"key1": "value1", "key2": 42, "key3": [1, 2, 3]},
        )
        debug(mock_logger, "message", kwargs=kwargs)

        assert len(mock_logger.calls) == 1
        call = mock_logger.calls[0]

        assert call["msg"] == "message"
        assert call["args"] == ()
        assert call["kwargs"] == asdict(kwargs)
