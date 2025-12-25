from unittest.mock import MagicMock, patch

from nnlogging.funcs import (
    add_task,
    advance_task,
    open_progress,
    recycle_progress,
    recycle_task,
    remove_task,
)
from nnlogging.options import ProgressFullOpt, TaskFullOpt


class MockTask:
    def __init__(self):
        self.finished = False


class MockProgress:
    def __init__(self):
        self._tasks = {}
        self.task_ids = []
        self.finished = False
        self.started = False
        self.stopped = False
        self.advances = []

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def stop_task(self, tid):
        if tid in self._tasks:
            self._tasks[tid].finished = True

    def remove_task(self, tid):
        if tid in self.task_ids:
            self.task_ids.remove(tid)
        if tid in self._tasks:
            del self._tasks[tid]

    def advance(self, tid, val):
        self.advances.append((tid, val))

    def add_task(self, **kwargs):
        tid = len(self.task_ids)
        self.task_ids.append(tid)
        self._tasks[tid] = MockTask()
        return tid


@patch("nnlogging.funcs._task.get_rprogress")
def test_open_progress(mock_get_rprogress):
    mock_prog = MockProgress()
    mock_get_rprogress.return_value = mock_prog

    branches = {
        "br1": {"console": MagicMock()},
        "br2": {"console": MagicMock(), "progress": MockProgress()},  # already exists
    }
    kwargs = ProgressFullOpt()

    open_progress(branches, kwargs)

    # br1 should have progress set and started
    assert "progress" in branches["br1"]
    assert branches["br1"]["progress"].started
    mock_get_rprogress.assert_called_once_with(branches["br1"]["console"], kwargs)

    # br2 should not be overwritten
    assert branches["br2"]["progress"] is not mock_prog


def test_recycle_task():
    prog = MockProgress()
    prog.add_task()  # tid 0
    prog.add_task()  # tid 1

    branches = {
        "br1": {
            "tasks": {"task1": 0, "task2": 1},
            "progress": prog,
        }
    }

    # Set task1 as finished
    prog._tasks[0].finished = True

    recycle_task(branches, "task1")
    recycle_task(branches, "task2")

    # task1 should be removed, task2 should remain
    assert "task1" not in branches["br1"]["tasks"]
    assert "task2" in branches["br1"]["tasks"]


def test_recycle_progress():
    prog1 = MockProgress()
    prog1.finished = True
    prog2 = MockProgress()

    branches = {
        "br1": {"progress": prog1},
        "br2": {"progress": prog2},
    }

    recycle_progress(branches)

    # prog1 should be stopped and removed
    assert "progress" not in branches["br1"]
    assert prog1.stopped

    # prog2 should remain
    assert "progress" in branches["br2"]


def test_add_task():
    prog = MockProgress()
    branches = {"br1": {"progress": prog, "tasks": {}}}
    kwargs = TaskFullOpt(total=None)

    add_task(branches, "task1", kwargs)

    assert branches["br1"]["tasks"]["task1"] == 0


def test_remove_task():
    prog = MockProgress()
    prog.add_task()  # tid 0

    branches = {"br1": {"progress": prog, "tasks": {"task1": 0}}}

    remove_task(branches, "task1")

    assert "task1" not in branches["br1"]["tasks"]
    assert 0 not in prog.task_ids
    assert 0 not in prog._tasks


def test_advance_task():
    prog = MockProgress()
    prog.add_task()  # tid 0

    branches = {"br1": {"progress": prog, "tasks": {"task1": 0}}}

    advance_task(branches, "task1", 1.0)

    assert prog.advances == [(0, 1.0)]
