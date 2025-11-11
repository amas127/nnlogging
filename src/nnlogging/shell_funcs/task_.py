from dataclasses import asdict

from nnlogging.exceptions import call_task_exists_error, call_task_not_found_error
from nnlogging.options import RichProgressOptionDict, TaskOptionDict
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ShellProtocol
from nnlogging.utils.factories import get_rich_progress
from nnlogging.utils.helpers import filter_by_typeddict

__all__ = [
    "task_add",
    "task_remove",
    "advance",
]


def _task_open(
    inst: ShellProtocol,
    name: str,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            e = call_task_exists_error(
                inst,
                branch_name,
                name,
                stacklevel=2,
            )
            if inst.strict:
                raise e

        else:
            if branch["progress"] is None:
                progress = get_rich_progress(
                    branch["console"],
                    **filter_by_typeddict(
                        asdict(inst.branch_config),
                        RichProgressOptionDict,
                    ),
                )
                progress.start()
                branch["progress"] = progress


def _task_close(
    inst: ShellProtocol,
    name: str,
):
    _task_found = False
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            _task_found = True
            assert branch["progress"] is not None  # definitely
            task_id = branch["tasks"][name]
            if branch["progress"]._tasks[task_id].finished:  # pyright: ignore[reportPrivateUsage]
                del branch["tasks"][name]
            if branch["progress"].finished:
                branch["progress"].stop()
                branch["progress"] = None
    if not _task_found:
        e = call_task_not_found_error(
            inst,
            name,
            stacklevel=2,
        )
        if inst.strict:
            raise e


def task_add(
    inst: ShellProtocol,
    name: str,
    **kwargs: Unpack[TaskOptionDict],
):
    _task_open(inst, name)
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        assert branch["progress"] is not None
        task_id = branch["progress"].add_task(**kwargs)  # pyright: ignore[reportArgumentType]
        branch["tasks"][name] = task_id


def task_remove(
    inst: ShellProtocol,
    name: str,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        if name in branch["tasks"]:
            assert branch["progress"] is not None
            task_id = branch["tasks"][name]
            branch["progress"]._tasks[task_id].finished_time = 0  # pyright: ignore[reportPrivateUsage]
    _task_close(inst, name)


def advance(
    inst: ShellProtocol,
    name: str,
    value: float,
):
    for branch_name in inst.branches:
        branch = inst.branches[branch_name]
        assert branch["progress"] is not None
        task_id = branch["tasks"][name]
        branch["progress"].advance(
            task_id=task_id,
            advance=value,
        )
    _task_close(inst, name)
