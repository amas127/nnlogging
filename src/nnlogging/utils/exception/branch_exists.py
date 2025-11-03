import sys

from nnlogging.shell_protocol import ShellProtocol
from nnlogging.typings import BranchExistsError, LogOptions
from nnlogging.utils.helpers import get__debugging, get_name

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never


def _branch_exists_msg(
    inst: ShellProtocol,
    name: str,
    /,
):
    return f'branch "{name}" already exists in {get_name(inst)}.branches'


def _branch_exists_error(
    inst: ShellProtocol,
    name: str,
    /,
):
    return BranchExistsError(
        f'branch "{name}" already exists in {get_name(inst)}.branches: {inst.branches}'
    )


def raise_branch_exists_error(
    inst: ShellProtocol,
    name: str,
    /,
    *,
    stacklevel: int = 1,
) -> Never:
    try:
        raise _branch_exists_error(inst, name)
    except BranchExistsError as e:
        inst.exception(
            _branch_exists_msg(inst, name),
            log_options=LogOptions(
                exc_info=e,
                stack_info=get__debugging(inst),
                stacklevel=stacklevel + 1,
            ),
        )
        raise
