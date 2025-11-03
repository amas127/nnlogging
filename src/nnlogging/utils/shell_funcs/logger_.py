import logging

from rich.console import ConsoleRenderable as RichConsoleRenderable

from nnlogging.shell_protocol import ShellProtocol
from nnlogging.typings import ConsolePrintOptions, LogOptions, Omitable
from nnlogging.utils.factory_funcs.shell_ import LoggerConfig, get_logging_logger
from nnlogging.utils.helpers import evolve_


def _logger_open(
    inst: ShellProtocol,
    /,
):
    if inst.logger is None:
        logging.captureWarnings(True)
        inst.logger = get_logging_logger(inst.logger_config)
        for name in inst.branches:
            branch = inst.branches[name]
            inst.logger.addHandler(branch["handler"])
            # TODO: add `filter` support in v0.2.0


def _logger_close(
    inst: ShellProtocol,
    /,
):
    if inst.logger is not None:
        logging.captureWarnings(False)
        for handler in inst.logger.handlers[:]:
            inst.logger.removeHandler(handler)
            handler.close()
        # TODO: add `filter` support in v0.2.0
        # inst.logger.filters.clear()
        inst.logger.setLevel(logging.NOTSET)
        inst.logger.propagate = False
        inst.logger = None


def logger_configure(
    inst: ShellProtocol,
    /,
    config: LoggerConfig | None = None,
    *,
    name: Omitable[str] = ...,
    level: Omitable[int | str] = ...,
    propagate: Omitable[bool] = ...,
):
    _logger_close(inst)
    inst.logger_config = evolve_(
        config or inst.logger_config,
        name=name,
        level=level,
        propagate=propagate,
    )


def log(
    inst: ShellProtocol,
    /,
    level: int,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    _logger_open(inst)
    assert inst.logger is not None
    match msg:
        case RichConsoleRenderable():
            debug(
                inst,
                f"Sending {repr(msg)} to branches ...",
                log_options=log_options or LogOptions(),
            )
            for name in inst.branches:
                branch = inst.branches[name]
                if level >= inst.logger.level and level >= branch["handler"].level:
                    branch["console"].print(
                        msg,
                        *args,
                        **(console_options or ConsolePrintOptions()),
                    )
        case _:
            inst.logger.log(
                level,
                msg,
                *args,
                **(log_options or LogOptions()),
            )


def debug(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    log(
        inst,
        logging.DEBUG,
        msg,
        *args,
        log_options=log_options,
        console_options=console_options,
    )


def info(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    log(
        inst,
        logging.INFO,
        msg,
        *args,
        log_options=log_options,
        console_options=console_options,
    )


def warn(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    log(
        inst,
        logging.WARNING,
        msg,
        *args,
        log_options=log_options,
        console_options=console_options,
    )


def error(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    log(
        inst,
        logging.ERROR,
        msg,
        *args,
        log_options=log_options,
        console_options=console_options,
    )


def critical(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    log(
        inst,
        logging.CRITICAL,
        msg,
        *args,
        log_options=log_options,
        console_options=console_options,
    )


def exception(
    inst: ShellProtocol,
    /,
    msg: object,
    *args: object,
    log_options: LogOptions | None = None,
    console_options: ConsolePrintOptions | None = None,
):
    default_log_options = LogOptions(exc_info=True)
    log(
        inst,
        logging.CRITICAL,
        msg,
        *args,
        log_options=default_log_options | (log_options or LogOptions()),
        console_options=console_options,
    )
