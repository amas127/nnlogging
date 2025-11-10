from nnlogging.options import LogOptionDict
from nnlogging.typings.exts import Never, Unpack
from nnlogging.typings.protocols import ExceptionProtocol
from nnlogging.utils.helpers import (
    get_name,
    inc_stacklevel,
    inject_excinfo,
)


class BranchExistsError(LookupError): ...


def raise_branch_exists_error(
    inst: ExceptionProtocol,
    name: str,
    /,
    **kwargs: Unpack[LogOptionDict],
) -> Never:
    try:
        raise BranchExistsError(
            f'branch "{name}" already exists in {get_name(inst)}.branches: {inst.branches}'
        )
    except BranchExistsError as e:
        inst.exception(
            'branch "%s" already exists in %s.branches',
            name,
            get_name(inst),
            **inc_stacklevel(inject_excinfo(kwargs, e)),
        )
        raise
