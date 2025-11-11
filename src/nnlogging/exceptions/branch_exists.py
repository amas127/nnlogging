from nnlogging.options import LogOptionDict
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ExceptionProtocol
from nnlogging.utils.helpers import (
    get_name,
    inc_stacklevel,
    inject_excinfo,
)


class BranchExistsError(LookupError): ...


def call_branch_exists_error(
    inst: ExceptionProtocol,
    name: str,
    /,
    **kwargs: Unpack[LogOptionDict],
):
    e = BranchExistsError(
        f'branch "{name}" already exists in {get_name(inst)}.branches: {inst.branches}'
    )
    inst.exception(
        'branch "%s" already exists in %s.branches',
        name,
        get_name(inst),
        **inc_stacklevel(inject_excinfo(kwargs, e)),
    )
    return e
