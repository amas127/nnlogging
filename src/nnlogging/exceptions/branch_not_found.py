from nnlogging.options import LogOptionDict
from nnlogging.typings.exts import Never, Unpack
from nnlogging.typings.protocols import ExceptionProtocol
from nnlogging.utils.helpers import (
    get_name,
    inc_stacklevel,
    inject_excinfo,
)


class BranchNotFoundError(LookupError): ...


def raise_branch_not_found_error(
    inst: ExceptionProtocol,
    name: str,
    /,
    **kwargs: Unpack[LogOptionDict],
) -> Never:
    try:
        raise BranchNotFoundError(
            f'branch "{name}" not found in {get_name(inst)}.branches: {inst.branches}'
        )
    except BranchNotFoundError as e:
        inst.exception(
            'branch "%s" not found in %s.branches',
            name,
            get_name(inst),
            **inc_stacklevel(inject_excinfo(kwargs, e)),
        )
        raise
