import logging
from collections.abc import Collection
from pathlib import Path
from threading import Lock

import nnlogging.funcs as _f
from nnlogging.helpers import get_duckcon, get_level, inc_stacklevel
from nnlogging.options import (
    BranchParOpt,
    CapexcParOpt,
    CapwarnFullOpt,
    CapwarnParOpt,
    ConsoleFullOpt,
    ConsoleParOpt,
    FilterFullOpt,
    FilterParOpt,
    HandlerFullOpt,
    HandlerParOpt,
    HandlerSetupFullOpt,
    LogFullOpt,
    LogParOpt,
    LoggerFullOpt,
    LoggerParOpt,
    ProgressFullOpt,
    ProgressParOpt,
    ProgressSetupFullOpt,
    RenderFullOpt,
    RenderParOpt,
    RunFullOpt,
    RunParOpt,
    TaskFullOpt,
    TaskParOpt,
)
from nnlogging.typings import (
    Artifact,
    Branches,
    DuckConnection,
    ExperimentRun,
    Jsonlike,
    Level,
    RichConsoleRenderable,
    Sink,
    Status,
    StepTrack,
    StrPath,
    Unpack,
)
from nnlogging.utils import (
    check_branch_found,
    check_branch_not_exists,
    check_task_found,
    check_task_not_exists,
)


__all__ = ["Shell"]


class Shell:  # noqa: PLR0904
    def __init__(  # noqa: PLR0913
        self,
        name: str = "nnlogging",
        *,
        console_opt: ConsoleParOpt | None = None,
        handler_opt: HandlerParOpt | None = None,
        filter_opt: FilterParOpt | None = None,
        progress_opt: ProgressParOpt | None = None,
        log_opt: LogParOpt | None = None,
        render_opt: RenderParOpt | None = None,
        capture_warning_opt: CapwarnParOpt | None = None,
        capture_exception_opt: CapexcParOpt | None = None,
        run_opt: RunParOpt | None = None,
    ) -> None:
        self.name: str = name
        self.branches: Branches = {}
        self.lock: Lock = Lock()

        self.console_opt: ConsoleParOpt = console_opt or {}
        self.handler_opt: HandlerParOpt = handler_opt or {}
        self.filter_opt: FilterParOpt = filter_opt or {}
        self.progress_opt: ProgressParOpt = progress_opt or {}
        self.log_opt: LogParOpt = log_opt or {}
        self.render_opt: RenderParOpt = render_opt or {}
        self.capture_warning_opt: CapwarnParOpt = capture_warning_opt or {}
        self.capture_exception_opt: CapexcParOpt = capture_exception_opt or {}

        self.run_opt: RunParOpt | None = run_opt
        self.db_connection: DuckConnection | None = None
        self.storage_dir: Path | None = None

        if self.run_opt:
            self.configure_run(**self.run_opt)

    def configure_console(
        self, **kwargs: Unpack[ConsoleParOpt]
    ) -> None:  # pragma: no cover
        self.console_opt |= kwargs

    def configure_handler(
        self, **kwargs: Unpack[HandlerParOpt]
    ) -> None:  # pragma: no cover
        self.handler_opt |= kwargs

    def configure_filter(
        self, **kwargs: Unpack[FilterParOpt]
    ) -> None:  # pragma: no cover
        self.filter_opt |= kwargs

    def configure_progress(
        self, **kwargs: Unpack[ProgressParOpt]
    ) -> None:  # pragma: no cover
        self.progress_opt |= kwargs

    def configure_log(self, **kwargs: Unpack[LogParOpt]) -> None:  # pragma: no cover
        self.log_opt |= kwargs

    def configure_render(
        self, **kwargs: Unpack[RenderParOpt]
    ) -> None:  # pragma: no cover
        self.render_opt |= kwargs

    def configure_capture_warning(
        self, **kwargs: Unpack[CapwarnParOpt]
    ) -> None:  # pragma: no cover
        self.capture_warning_opt |= kwargs

    def configure_capture_exception(
        self, **kwargs: Unpack[CapexcParOpt]
    ) -> None:  # pragma: no cover
        self.capture_exception_opt |= kwargs

    @staticmethod
    def configure_logger(
        loggers: Collection[str | None], **kwargs: Unpack[LoggerParOpt]
    ) -> None:
        logger_opt = LoggerFullOpt(**kwargs)
        for lname in loggers:
            logger = logging.getLogger(lname)
            logger.setLevel(get_level(logger_opt.level))
            logger.propagate = logger_opt.propagate

    def configure_run(self, **kwargs: Unpack[RunParOpt]) -> None:
        with self.lock:
            self.run_opt = self.run_opt | kwargs if self.run_opt else kwargs
            run_opt = RunFullOpt(**self.run_opt)
            if storage_dir := _f.find_storage_dir(run_opt.storage_dir):
                self.storage_dir = storage_dir
            else:
                self.storage_dir = Path.cwd() / run_opt.storage_dir
                self.storage_dir.mkdir(parents=True, exist_ok=True)
                artifacts_dir = self.storage_dir / run_opt.artifacts_dir
                artifacts_dir.mkdir(parents=True, exist_ok=True)
            self.db_connection = get_duckcon(self.storage_dir / run_opt.tables_file)
            _f.create_tables(self.db_connection)
            _f.create_run(
                self.db_connection,
                run_opt.uuid,
                ExperimentRun(
                    grp=run_opt.group, exp=run_opt.experiment, run=run_opt.run
                ),
                parents=run_opt.parents,
            )

    def add_branch(
        self,
        *sinks: tuple[str, Sink],
        logger: str | None,
        **kwargs: Unpack[BranchParOpt],
    ) -> None:
        console_fields = ConsoleParOpt.__annotations__.keys()
        handler_fields = HandlerParOpt.__annotations__.keys()
        filter_fields = FilterParOpt.__annotations__.keys()
        console_opt = self.console_opt.copy()
        handler_opt = self.handler_opt.copy()
        filter_opt = self.filter_opt.copy()

        for k, v in kwargs.items():
            if k in console_fields:
                console_opt[k] = v
            elif k in handler_fields:
                handler_opt[k] = v
            elif k in filter_fields:
                filter_opt[k] = v
            else:
                raise KeyError

        handler_setup_fields = HandlerSetupFullOpt.__dataclass_fields__.keys()
        handler_setup_opt = {
            k: v for k, v in handler_opt.items() if k in handler_setup_fields
        }
        handler_msgfmt_opt = handler_opt.get("log_message_format", None)
        with self.lock:
            if not all(check_branch_not_exists(self.branches, s[0]) for s in sinks):
                return
            _f.add_branch(
                self.branches,
                sinks,
                logger,
                ConsoleFullOpt(**console_opt),
                HandlerFullOpt(
                    setup=HandlerSetupFullOpt(**handler_setup_opt),  # pyright: ignore[reportArgumentType]
                    msgfmt=handler_msgfmt_opt,
                ),
                FilterFullOpt(**filter_opt),
            )

    def remove_branch(self, *names: str) -> None:
        with self.lock:
            if not all(check_branch_found(self.branches, n) for n in names):
                return
            _f.remove_branch(self.branches, names)

    def capture_warnings(self, **kwargs: Unpack[CapwarnParOpt]) -> None:
        _f.capture_warnings(CapwarnFullOpt(**(self.capture_warning_opt | kwargs)))

    def add_task(self, name: str, **kwargs: Unpack[TaskParOpt]) -> None:
        progress_setup_fields = ProgressSetupFullOpt.__dataclass_fields__.keys()
        progress_setup_opt = {
            k: v for k, v in self.progress_opt.items() if k in progress_setup_fields
        }
        progress_columns_opt = self.progress_opt.get("columns", None)
        with self.lock:
            if not check_task_not_exists(self.branches, name):
                return
            _f.open_progress(
                self.branches,
                ProgressFullOpt(
                    setup=ProgressSetupFullOpt(**progress_setup_opt),  # pyright: ignore[reportArgumentType]
                    columns=progress_columns_opt,
                ),
            )
            _f.add_task(self.branches, name, TaskFullOpt(**kwargs))

    def remove_task(self, name: str) -> None:
        with self.lock:
            if not check_task_found(self.branches, name):
                return
            _f.remove_task(self.branches, name)
            _f.recycle_progress(self.branches)

    def log(
        self,
        logger: str | None,
        level: Level,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.log(
            logging.getLogger(logger),
            get_level(level),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def debug(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.debug(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def info(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.info(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def warning(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.warning(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def error(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.error(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def critical(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.critical(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def exception(
        self,
        logger: str | None,
        msg: str,
        *args: object,
        **kwargs: Unpack[LogParOpt],
    ) -> None:  # pragma: no cover
        _f.exception(
            logging.getLogger(logger),
            msg,
            *args,
            kwargs=inc_stacklevel(LogFullOpt(**(self.log_opt | kwargs))),
        )

    def render(
        self,
        logger: str | None,
        level: str | int,
        *objs: RichConsoleRenderable,
        **kwargs: Unpack[RenderParOpt],
    ) -> None:  # pragma: no cover
        with self.lock:
            _f.render(
                self.branches,
                logging.getLogger(logger),
                get_level(level),
                *objs,
                kwargs=RenderFullOpt(**(self.render_opt | kwargs)),
            )

    def advance(self, task: str, value: float) -> None:
        _f.advance_task(self.branches, task, value)
        with self.lock:
            if not check_task_found(self.branches, task):
                return
            _f.recycle_task(self.branches, task)
            _f.recycle_progress(self.branches)

    def add_tags(self, *tags: str) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.add_tags(self.db_connection, run_opt.uuid, tags)

    def remove_tags(self, *tags: str) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.remove_tags(self.db_connection, run_opt.uuid, tags)

    def add_hparams(self, hparams: Jsonlike) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.add_hparams(self.db_connection, run_opt.uuid, hparams)

    def add_summaries(self, summaries: Jsonlike) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.add_summaries(self.db_connection, run_opt.uuid, summaries)

    def add_extras(self, extras: Jsonlike) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.add_extras(self.db_connection, run_opt.uuid, extras)

    def track(
        self,
        step: int,
        metrics: Jsonlike | None = None,
        artifacts: list[Artifact] | None = None,
        context: Jsonlike | None = None,
    ) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        _f.track(
            self.db_connection,
            self.run_opt["uuid"],
            step=step,
            item=StepTrack(met=metrics, atf=artifacts, ctx=context),
        )

    def track_artifact(
        self, step: int, *paths: StrPath, context: Jsonlike | None = None
    ) -> None:
        if not self.run_opt or not self.db_connection or not self.storage_dir:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.track_artifact(
            self.db_connection,
            run_opt.uuid,
            *paths,
            step=step,
            dstdir=self.storage_dir / run_opt.artifacts_dir,
            ctx=context,
        )

    def update_status(self, status: Status) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.update_status(self.db_connection, run_opt.uuid, status)

    def close_run(self) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.close_run(self.db_connection, run_opt.uuid)

    def archive_run(self) -> None:
        if not self.run_opt or not self.db_connection:
            raise ValueError
        run_opt = RunFullOpt(**self.run_opt)
        _f.archive_run(self.db_connection, run_opt.uuid)
