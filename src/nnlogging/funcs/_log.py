import logging

from nnlogging.helpers import asdict, inc_stacklevel, inj_excinfo
from nnlogging.options import LogFullOpt
from nnlogging.typings import Logger


__all__ = ["critical", "debug", "error", "exception", "info", "log", "warning"]


def log(
    logger: Logger, level: int, msg: str, *args: object, kwargs: LogFullOpt
) -> None:
    logger.log(level, msg, *args, **asdict(inc_stacklevel(kwargs)))


def debug(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.DEBUG, msg, *args, kwargs=inc_stacklevel(kwargs))


def info(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.INFO, msg, *args, kwargs=inc_stacklevel(kwargs))


def warning(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.WARNING, msg, *args, kwargs=inc_stacklevel(kwargs))


def error(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.ERROR, msg, *args, kwargs=inc_stacklevel(kwargs))


def critical(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.CRITICAL, msg, *args, kwargs=inc_stacklevel(kwargs))


def exception(logger: Logger, msg: str, *args: object, kwargs: LogFullOpt) -> None:
    log(logger, logging.ERROR, msg, *args, kwargs=inj_excinfo(inc_stacklevel(kwargs)))
