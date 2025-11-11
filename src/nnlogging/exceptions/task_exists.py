from nnlogging.options import LogOptionDict
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ExceptionProtocol
from nnlogging.utils.helpers import (
    get_name,
    inc_stacklevel,
    inject_excinfo,
)


class TaskExistsError(LookupError): ...


def call_task_exists_error(
    inst: ExceptionProtocol,
    branch: str,
    name: str,
    /,
    **kwargs: Unpack[LogOptionDict],
):
    e = TaskExistsError(
        f'task "{name}" already exists in {get_name(inst)}.branches."{branch}"."tasks": {inst.branches[branch]["tasks"]}'
    )
    inst.exception(
        'task "%s" already exists in %s.branches."%s"."tasks"',
        name,
        get_name(inst),
        branch,
        **inc_stacklevel(inject_excinfo(kwargs, e)),
    )
    return e
