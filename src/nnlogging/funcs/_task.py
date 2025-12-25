from nnlogging.options import ProgressFullOpt, TaskFullOpt
from nnlogging.typings import Branches
from nnlogging.utils import get_rprogress, get_rtask


__all__ = [
    "add_task",
    "advance_task",
    "open_progress",
    "recycle_progress",
    "recycle_task",
    "remove_task",
]


def open_progress(branches: Branches, kwargs: ProgressFullOpt) -> None:
    for br in branches.values():  # MAYBE: allow to use progress or not by branches
        if "progress" not in br:
            br["progress"] = get_rprogress(br["console"], kwargs)
            br["progress"].start()


def recycle_task(branches: Branches, task: str) -> None:
    for br in branches.values():
        tid, prog = br["tasks"].get(task), br.get("progress")
        if tid is not None and prog and prog._tasks[tid].finished:  # noqa: SLF001
            prog.stop_task(tid)
            del br["tasks"][task]


def recycle_progress(branches: Branches) -> None:
    for br in branches.values():
        if (prog := br.get("progress")) and prog.finished:
            prog.stop()
            del br["progress"]


def add_task(branches: Branches, task: str, kwargs: TaskFullOpt) -> None:
    for br in branches.values():
        if prog := br.get("progress"):
            br["tasks"][task] = get_rtask(prog, kwargs)


def remove_task(branches: Branches, task: str) -> None:
    for br in branches.values():
        if (tid := br["tasks"].get(task)) is not None:
            if (prog := br.get("progress")) and tid in prog.task_ids:
                prog.stop_task(tid)
                prog.remove_task(tid)
            del br["tasks"][task]


def advance_task(branches: Branches, task: str, value: float) -> None:
    # MAYBE: caching hot tuple[RichProgress, RichTaskID] for performance reason
    for br in branches.values():
        if (tid := br["tasks"].get(task)) is not None and (prog := br.get("progress")):
            prog.advance(tid, value)
