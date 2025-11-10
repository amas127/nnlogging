from nnlogging.options import LogOptionDict
from nnlogging.typings.exts import Never, Unpack
from nnlogging.typings.protocols import ExceptionProtocol
from nnlogging.utils.helpers import (
    get_name,
    inc_stacklevel,
    inject_excinfo,
)


class TaskNotFoundError(LookupError): ...


def raise_task_not_found_error(
    inst: ExceptionProtocol,
    name: str,
    /,
    **kwargs: Unpack[LogOptionDict],
) -> Never:
    try:
        raise TaskNotFoundError(
            f'task "{name}" not found in {get_name(inst)}.branches: {inst.branches}'
        )
    except TaskNotFoundError as e:
        inst.exception(
            'task "%s" not found in %s.branches',
            name,
            get_name(inst),
            **inc_stacklevel(inject_excinfo(kwargs, e)),
        )
        raise
