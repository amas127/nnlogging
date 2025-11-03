"""
``nnlogging.utils``
"""

from .exception import (
    raise_branch_exists_error,
    raise_branch_not_found_error,
    raise_task_exists_error,
    raise_task_not_found_error,
)
from .factory_funcs.rich_ import (
    get_rich_console,
    get_rich_handler,
    get_rich_progress,
    get_rich_progress_default_columns,
)
from .factory_funcs.shell_ import (
    BranchConfig,
    LoggerConfig,
    RunConfig,
    get_aim_run,
    get_branch,
    get_logging_logger,
)
from .helpers import evolve_, get__debugging, get_name, or_
from .shell_funcs.branch_ import branch_add, branch_configure, branch_remove
from .shell_funcs.logger_ import (
    critical,
    debug,
    error,
    exception,
    info,
    log,
    logger_configure,
    warn,
)
from .shell_funcs.run_ import add_tag, remove_tag, run_configure, track, update_metadata
from .shell_funcs.task_ import advance, task_add, task_remove

__all__ = [
    # helper
    "evolve_",
    "or_",
    "get__debugging",
    "get_name",
    # rich factory
    "get_rich_console",
    "get_rich_handler",
    "get_rich_progress",
    "get_rich_progress_default_columns",
    # shell factory
    "LoggerConfig",
    "get_logging_logger",
    "RunConfig",
    "get_aim_run",
    "BranchConfig",
    "get_branch",
    # shell func
    "branch_add",
    "branch_configure",
    "branch_remove",
    "critical",
    "debug",
    "error",
    "exception",
    "info",
    "log",
    "logger_configure",
    "warn",
    "add_tag",
    "remove_tag",
    "run_configure",
    "track",
    "update_metadata",
    "advance",
    "task_add",
    "task_remove",
    # exception
    "raise_branch_exists_error",
    "raise_branch_not_found_error",
    "raise_task_exists_error",
    "raise_task_not_found_error",
]
