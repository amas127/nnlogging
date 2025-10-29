import sys

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never


from nnlogging.shell.protocol import ShellProtocol
from nnlogging.typings import BranchNotFoundError, LogOptions
from nnlogging.utils import get__debugging, get_name


def _branch_not_found_msg(
    inst: ShellProtocol,
    name: str,
    /,
):
    return f'branch "{name}" not found in {get_name(inst)}.branches'


def _branch_not_found_error(
    inst: ShellProtocol,
    name: str,
    /,
):
    return BranchNotFoundError(
        f'branch "{name}" not found in {get_name(inst)}.branches: {inst.branches}'
    )


def raise_branch_not_found_error(
    inst: ShellProtocol,
    name: str,
    /,
    *,
    stacklevel: int = 1,
) -> Never:
    try:
        raise _branch_not_found_error(inst, name)
    except BranchNotFoundError as e:
        inst.exception(
            _branch_not_found_msg(inst, name),
            log_options=LogOptions(
                exc_info=e,
                stack_info=get__debugging(inst),
                stacklevel=stacklevel + 1,
            ),
        )
        raise
