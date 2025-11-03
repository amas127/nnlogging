import sys

from nnlogging.shell_protocol import ShellProtocol
from nnlogging.typings import LogOptions, TaskExistsError
from nnlogging.utils.helpers import get__debugging, get_name

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never


def _task_exists_msg(
    inst: ShellProtocol,
    branch: str,
    name: str,
    /,
):
    return (
        f'task "{name}" already exists in {get_name(inst)}.branches."{branch}"."tasks"'
    )


def _task_exists_error(
    inst: ShellProtocol,
    branch: str,
    name: str,
    /,
):
    return TaskExistsError(
        f'task "{name}" already exists in {get_name(inst)}.branches."{branch}"."tasks": {inst.branches[branch]["tasks"]}'
    )


def raise_task_exists_error(
    inst: ShellProtocol,
    branch: str,
    name: str,
    /,
    *,
    stacklevel: int = 1,
) -> Never:
    try:
        raise _task_exists_error(inst, branch, name)
    except TaskExistsError as e:
        inst.exception(
            _task_exists_msg(inst, branch, name),
            log_options=LogOptions(
                exc_info=e,
                stack_info=get__debugging(inst),
                stacklevel=stacklevel + 1,
            ),
        )
        raise
