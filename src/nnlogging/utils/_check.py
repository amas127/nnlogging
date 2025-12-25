from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING

from nnlogging.exceptions import (
    BranchExistsError,
    BranchNotFoundError,
    RunNotFoundError,
    RunUpdateArchivedError,
    TaskExistsError,
    TaskNotFoundError,
)


if TYPE_CHECKING:
    from uuid import UUID

    from nnlogging.typings import Branches, DuckConnection, ExcCallback


__all__ = [
    "check_branch_found",
    "check_branch_not_exists",
    "check_exprun_updatable",
    "check_task_found",
    "check_task_not_exists",
]


def check_task_not_exists(
    branches: Branches,
    task: str,
    *,
    exc_raise: bool = True,
    exc_callback: ExcCallback | None = None,
) -> bool:
    for brn, br in branches.items():
        if task in br["tasks"]:
            e = TaskExistsError(task, (brn, br))
            if exc_callback:
                exc_callback(
                    "Task '%s' already exists in branch '%s'", task, brn, exc_info=e
                )
            if exc_raise:
                raise e
            return False
    return True


def check_task_found(
    branches: Branches,
    task: str,
    *,
    exc_raise: bool = True,
    exc_callback: ExcCallback | None = None,
) -> bool:
    if not any(task in br["tasks"] for br in branches.values()):
        e = TaskNotFoundError(task, branches.values())
        if exc_callback:
            exc_callback("Task '%s' not found in branches", task, exc_info=e)
        if exc_raise:
            raise e
        return False
    return True


def check_branch_not_exists(
    branches: Branches,
    qbranch: str,
    *,
    exc_raise: bool = True,
    exc_callback: ExcCallback | None = None,
) -> bool:
    if qbranch in branches:
        e = BranchExistsError(qbranch, branches)
        if exc_callback:
            exc_callback("Branch '%s' already exists in branches", qbranch, exc_info=e)
        if exc_raise:
            raise e
        return False
    return True


def check_branch_found(
    branches: Branches,
    qbranch: str,
    *,
    exc_raise: bool = True,
    exc_callback: ExcCallback | None = None,
) -> bool:
    if qbranch not in branches:
        e = BranchNotFoundError(qbranch, branches)
        if exc_callback:
            exc_callback("Branch '%s' not found in branches", qbranch, exc_info=e)
        if exc_raise:
            raise e
        return False
    return True


@lru_cache
def _sqlstr_select_archived() -> str:
    with Path(__file__).parent.joinpath("select_archived.sql").open("r") as f:
        return f.read()


def check_exprun_updatable(
    con: DuckConnection,
    uuid: UUID,
    *,
    exc_raise: bool = True,
    exc_callback: ExcCallback | None = None,
) -> bool:
    res = con.execute(_sqlstr_select_archived(), (uuid,)).fetchall()
    if not res:
        e = RunNotFoundError(uuid)
    elif res[0][0]:
        e = RunUpdateArchivedError(uuid)
    else:
        return True
    if exc_callback:
        exc_callback("Run '%s' cannot be updated", uuid.hex, exc_info=e)
    if exc_raise:
        raise e
    return False
