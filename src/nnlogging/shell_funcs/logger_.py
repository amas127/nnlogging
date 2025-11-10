import logging
from dataclasses import asdict, replace

from rich.console import ConsoleRenderable as RichConsoleRenderable

from nnlogging.options import (
    LoggerConfigOptionDict,
    LoggingLogOptionDict,
    LogOptionDict,
    RichPrintOptionDict,
)
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ShellProtocol
from nnlogging.utils.factories import get_logging_logger
from nnlogging.utils.helpers import (
    filter_by_typeddict,
    inc_stacklevel,
    inject_excinfo,
)

__all__ = [
    "logger_configure",
    "log",
    "debug",
    "info",
    "warn",
    "error",
    "critical",
    "exception",
]


def _logger_open(
    inst: ShellProtocol,
):
    if inst.logger is None:
        logging.captureWarnings(True)
        inst.logger = get_logging_logger(**asdict(inst.logger_config))
        for name in inst.branches:
            branch = inst.branches[name]
            inst.logger.addHandler(branch["handler"])
            # TODO: add `filter` support in v0.2.0


def _logger_close(
    inst: ShellProtocol,
):
    if inst.logger is not None:
        logging.captureWarnings(False)
        for handler in inst.logger.handlers[:]:
            inst.logger.removeHandler(handler)
            handler.close()
        inst.logger.filters.clear()
        inst.logger.setLevel(logging.NOTSET)
        inst.logger.propagate = True
        inst.logger = None


def logger_configure(
    inst: ShellProtocol,
    **kwargs: Unpack[LoggerConfigOptionDict],
):
    _logger_close(inst)
    inst.logger_config = replace(
        inst.logger_config,
        **kwargs,
    )


def log(
    inst: ShellProtocol,
    level: int,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    _logger_open(inst)
    assert inst.logger is not None
    match msg:
        case RichConsoleRenderable():
            inst.logger.log(
                level,
                "Sending %s to %s branches ...",
                msg,
                inst,
                **inc_stacklevel(filter_by_typeddict(kwargs, LoggingLogOptionDict)),
            )
            for name in inst.branches:
                branch = inst.branches[name]
                if level >= inst.logger.level and level >= branch["handler"].level:
                    branch["console"].print(
                        msg,
                        *args,
                        **filter_by_typeddict(kwargs, RichPrintOptionDict),
                    )
        case _:
            inst.logger.log(
                level,
                msg,
                *args,
                **inc_stacklevel(filter_by_typeddict(kwargs, LoggingLogOptionDict)),
            )


def debug(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.DEBUG,
        msg,
        *args,
        **inc_stacklevel(kwargs),
    )


def info(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.INFO,
        msg,
        *args,
        **inc_stacklevel(kwargs),
    )


def warn(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.WARN,
        msg,
        *args,
        **inc_stacklevel(kwargs),
    )


def error(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.ERROR,
        msg,
        *args,
        **inc_stacklevel(kwargs),
    )


def critical(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.CRITICAL,
        msg,
        *args,
        **inc_stacklevel(kwargs),
    )


def exception(
    inst: ShellProtocol,
    msg: object,
    *args: object,
    **kwargs: Unpack[LogOptionDict],
):
    log(
        inst,
        logging.ERROR,
        msg,
        *args,
        **inc_stacklevel(inject_excinfo(kwargs)),
    )
