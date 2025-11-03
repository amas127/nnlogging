from nnlogging.shell_protocol import ShellProtocol
from nnlogging.utils.exception import (
    raise_task_exists_error,
    raise_task_not_found_error,
)
from nnlogging.utils.factory_funcs.rich_ import get_rich_progress


def _task_open(
    inst: ShellProtocol,
    /,
    name: str,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            raise_task_exists_error(
                inst,
                branch_name,
                name,
                stacklevel=2,
            )
        if branch["progress"] is None:
            progress = get_rich_progress(
                branch["console"],
                columns=inst.branch_config.columns,
                transient=inst.branch_config.transient,
                refresh_per_second=inst.branch_config.refresh_per_second,
                speed_estimate_period=inst.branch_config.speed_estimate_period,
                default_column_markup=inst.branch_config.default_column_markup,
            )
            progress.start()
            branch["progress"] = progress


def _task_close(
    inst: ShellProtocol,
    /,
    name: str,
):
    task_found = False
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            task_found = True
            assert branch["progress"] is not None  # definitely
            task_id = branch["tasks"][name]
            if branch["progress"]._tasks[task_id].finished:  # pyright: ignore[reportPrivateUsage]
                del branch["tasks"][name]
            if branch["progress"].finished:
                branch["progress"].stop()
                branch["progress"] = None
    if not task_found:
        raise_task_not_found_error(
            inst,
            name,
            stacklevel=2,
        )


def task_add(
    inst: ShellProtocol,
    /,
    name: str,
    *,
    desc: str,
    total: float | None,
    done: float = 0,
):
    _task_open(inst, name)
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        assert branch["progress"] is not None  # definitely
        task_id = branch["progress"].add_task(
            description=desc,
            total=total,
            completed=done,  # pyright: ignore[reportArgumentType]
        )
        branch["tasks"][name] = task_id


def task_remove(
    inst: ShellProtocol,
    /,
    name: str,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            assert branch["progress"] is not None  # definitely
            task_id = branch["tasks"][name]
            branch["progress"]._tasks[task_id].finished_time = 0  # pyright: ignore[reportPrivateUsage]
    _task_close(inst, name)


def advance(
    inst: ShellProtocol,
    /,
    name: str,
    *,
    advance: float,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        assert branch["progress"] is not None  # definitely
        task_id = branch["tasks"][name]
        branch["progress"].advance(
            task_id=task_id,
            advance=advance,
        )
    _task_close(inst, name)
