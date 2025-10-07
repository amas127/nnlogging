"""nnlog.shell"""

import logging
from collections.abc import Mapping
from logging import Handler, Logger

from aim import Run
from aim.sdk.types import AimObject
from rich.console import Console as RichConsole
from rich.console import ConsoleRenderable
from rich.progress import Progress as RichProgress
from rich.progress import TaskID

from .utils import (
    get_aim_run,
    get_rich_handler,
    get_rich_progress,
)

__all__ = ["Shell"]


class Shell:
    name: str = "nnlog"

    def __init__(
        self,
        name: str | None = None,
        level: int = logging.INFO,
        propagate: bool = False,
    ):
        self.name = name or self.name
        self.level: int = level
        self.propagate: bool = propagate

        self.logger: Logger = logging.getLogger(self.name)
        self.consoles: dict[str, RichConsole] = dict()
        self.handlers: dict[str, Handler] = dict()
        self.progresses: dict[str, RichProgress] = dict()
        self.tasks: dict[str, dict[str, TaskID]] = dict()
        self.aim_run: Run | None = None

        self.configure_logger()

    def configure_logger(
        self,
        level: int | None = None,
        propagate: bool | None = None,
    ):
        if level is not None:
            self.level = level
        if propagate is not None:
            self.propagate = propagate
        self.logger.setLevel(self.level)
        self.logger.propagate = self.propagate

    def add_console(
        self,
        consoles: Mapping[str, RichConsole],
    ):
        self.consoles.update(consoles)

    def add_handler(
        self,
        handlers: Mapping[str, Handler],
    ):
        self.handlers.update(handlers)

    def add_progress(
        self,
        progresses: Mapping[str, RichProgress],
    ):
        self.progresses.update(progresses)

    def build_handler_from_console(
        self,
        *names: str,
        **kwargs,
    ):
        if len(names) == 0:
            names = tuple(n for n in self.consoles.keys())

        handlers = {
            name: get_rich_handler(
                console=self.consoles[name],
                name=name,
                **kwargs,
            )
            for name in names
        }
        self.add_handler(handlers)
        self.sync_handlers()

    def build_progress_from_console(
        self,
        *names: str,
        **kwargs,
    ):
        if len(names) == 0:
            names = tuple(n for n in self.consoles.keys())

        progresses = {
            name: get_rich_progress(
                console=self.consoles[name],
                **kwargs,
            )
            for name in names
        }
        self.add_progress(progresses)

    def sync_handlers(self):
        self.logger.handlers.clear()
        for hdlr in self.handlers.values():
            self.logger.addHandler(hdlr)

    def add_task(
        self,
        task_name: str,
        description: str,
        start: bool = True,
        total: float | None = 100,
        completed: float = 0,
    ):
        self.tasks[task_name] = dict()
        for progress_name in self.progresses.keys():
            task_id = self.progresses[progress_name].add_task(
                description=description,
                start=start,
                total=total,
                completed=completed,  # pyright: ignore[reportArgumentType]
            )
            self.tasks[task_name].update({progress_name: task_id})

    def start_progress(self, *names: str):
        if len(names) == 0:
            names = tuple(n for n in self.progresses.keys())

        for name in names:
            self.progresses[name].start()

    def stop_progress(self, *names: str):
        if len(names) == 0:
            names = tuple(n for n in self.progresses.keys())

        for progress_name in names:
            self.progresses[progress_name].stop()
            del self.progresses[progress_name]
            for task_name in self.tasks.keys():
                del self.tasks[task_name][progress_name]

    def update_task(
        self,
        task_name: str,
        advance: float | None = None,
        total: float | None = None,
        completed: float | None = None,
    ):
        for progress_name, progress in self.progresses.items():
            task_id = self.tasks[task_name][progress_name]
            progress.update(
                task_id=task_id,
                advance=advance,
                total=total,
                completed=completed,
            )

    def log(
        self,
        level: int,
        msg: object,
        *args: object,
        stacklevel: int = 2,
        **kwargs,
    ):
        if isinstance(msg, ConsoleRenderable):
            self.debug(f"Parsing {msg} to consoles ...")
            for console in self.consoles.values():
                console.print(msg, *args, **kwargs)
            return

        self.logger.log(
            level=level,
            msg=msg,
            *args,
            stacklevel=stacklevel,
            **kwargs,
        )

    def debug(
        self,
        msg: object,
        *args: object,
        stacklevel: int = 3,
        **kwargs,
    ):
        self.log(
            logging.DEBUG,
            msg,
            *args,
            stacklevel=stacklevel,
            **kwargs,
        )

    def info(
        self,
        msg: object,
        *args: object,
        stacklevel: int = 3,
        **kwargs,
    ):
        self.log(
            logging.INFO,
            msg,
            *args,
            stacklevel=stacklevel,
            **kwargs,
        )

    def warn(
        self,
        msg: object,
        *args: object,
        stacklevel: int = 3,
        **kwargs,
    ):
        self.log(
            logging.WARN,
            msg,
            *args,
            stacklevel=stacklevel,
            **kwargs,
        )

    def error(
        self,
        msg: object,
        *args: object,
        stacklevel: int = 3,
        **kwargs,
    ):
        self.log(
            logging.ERROR,
            msg,
            *args,
            stacklevel=stacklevel,
            **kwargs,
        )

    def exception(
        self,
        msg: object,
        *args,
        exc_info: bool = True,
        stacklevel: int = 3,
        **kwargs,
    ):
        self.log(
            logging.ERROR,
            msg,
            *args,
            exc_info=exc_info,
            stacklevel=stacklevel,
            **kwargs,
        )

    def add_aimrun(
        self,
        **kwargs,
    ):
        self.aim_run = get_aim_run(**kwargs)

    def update_aimrun_metadata(
        self,
        label: str,
        metadata: dict[str, object],
    ):
        if self.aim_run is None:
            self.error(
                "`aim_run` is not initialized",
                stacklevel=4,
                exc_info=ValueError(f"`aim_run` is {self.aim_run}"),
            )
        else:
            self.aim_run[label] = metadata

    def track(
        self,
        value: object,
        name: str,
        step: int | None = None,
        epoch: int | None = None,
        context: AimObject | None = None,
    ):
        if self.aim_run is None:
            self.error(
                "`aim_run` is not initialized",
                stacklevel=4,
                exc_info=ValueError(f"`aim_run` is {self.aim_run}"),
            )
        else:
            self.aim_run.track(
                value,
                name=name,
                step=step,
                epoch=epoch,
                context=context,
            )
