from math import ceil

import pytest
from rich.progress import Progress as RichProgress

from nnlogging.exceptions import TaskExistsError, TaskNotFoundError
from nnlogging.shell import Shell


def test_task_add(
    task_name,
    task_desc,
    task_total,
):
    shell = Shell()
    shell.branch_add("default")
    assert "default" in shell.branches
    branch = shell.branches["default"]
    assert len(branch["tasks"]) == 0
    assert branch["progress"] is None
    shell.task_add(
        task_name,
        description=task_desc,
        total=task_total,
    )
    assert task_name in branch["tasks"]
    progress = branch["progress"]
    assert isinstance(progress, RichProgress)
    task_id = branch["tasks"][task_name]
    task = progress._tasks[task_id]
    assert task.total == task_total
    assert task.description == task_desc


def test_task_remove(
    task_name,
    task_desc,
    task_total,
):
    shell = Shell()
    shell.branch_add("default")
    assert "default" in shell.branches
    branch = shell.branches["default"]
    assert len(branch["tasks"]) == 0
    shell.task_add(
        task_name,
        description=task_desc,
        total=task_total,
    )
    assert task_name in branch["tasks"]
    assert isinstance(branch["progress"], RichProgress)
    shell.task_remove(task_name)
    assert task_name not in branch["tasks"]
    assert branch["progress"] is None


def test_task_add_duplicate(
    task_name_gen,
    task_desc_gen,
    task_total_gen,
):
    task_name = task_name_gen()
    shell = Shell(strict=True)
    shell.branch_add("default")
    shell.task_add(
        task_name,
        description=task_desc_gen(),
        total=task_total_gen(),
    )
    with pytest.raises(TaskExistsError):
        shell.task_add(
            task_name,
            description=task_desc_gen(),
            total=task_total_gen(),
        )


def test_task_remove_not_found(task_name_gen):
    shell = Shell(strict=True)
    shell.branch_add("default")
    with pytest.raises(TaskNotFoundError):
        shell.task_remove(task_name_gen())


def test_advance_limited(
    task_name,
    task_desc,
    task_total_limited,
    task_done,
    advance,
):
    shell = Shell()
    shell.branch_add("default")
    assert "default" in shell.branches
    branch = shell.branches["default"]
    assert len(branch["tasks"]) == 0
    shell.task_add(
        task_name,
        description=task_desc,
        total=task_total_limited,
        completed=task_done,
    )
    assert task_name in branch["tasks"]
    task_id = branch["tasks"][task_name]
    assert isinstance(branch["progress"], RichProgress)
    progress = branch["progress"]
    assert not progress.finished
    task = branch["progress"]._tasks[task_id]
    assert not task.finished

    ideal_count: int = ceil((task_total_limited - task_done) / advance)
    assert ideal_count > 0

    for _ in range(ideal_count - 1):
        shell.advance(task_name, advance)
        assert not task.finished
        assert not progress.finished
        assert task_name in branch["tasks"]
        assert isinstance(branch["progress"], RichProgress)

    shell.advance(task_name, advance)
    assert task.finished
    assert progress.finished
    assert task_name not in branch["tasks"]
    assert branch["progress"] is None


def test_advance_unlimited(
    task_name,
    task_desc,
    task_total_unlimited,
    task_done,
    advance,
):
    assert task_total_unlimited is None
    shell = Shell()
    shell.branch_add("default")
    assert "default" in shell.branches
    branch = shell.branches["default"]
    assert len(branch["tasks"]) == 0
    shell.task_add(
        task_name,
        description=task_desc,
        total=task_total_unlimited,
        completed=task_done,
    )
    assert task_name in branch["tasks"]
    task_id = branch["tasks"][task_name]
    assert isinstance(branch["progress"], RichProgress)
    progress = branch["progress"]
    assert not progress.finished
    task = branch["progress"]._tasks[task_id]
    assert not task.finished

    max_count = 20

    for _ in range(max_count):
        shell.advance(task_name, advance)
        assert not task.finished
        assert not progress.finished
        assert task_name in branch["tasks"]
        assert isinstance(branch["progress"], RichProgress)
