from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, final

from ._bases import (
    AlreadyExistsError,
    ArchivedError,
    BranchCtxError,
    CustomTypeError,
    LevelCtxError,
    NotFoundError,
    NullValueError,
    OutRangeError,
    RunCtxError,
    StacklevelCtxError,
    StepError,
    TaskCtxError,
    TrackCtxError,
    WeirdError,
)


if TYPE_CHECKING:
    from collections.abc import Collection
    from uuid import UUID

    from nnlogging.typings import Branch, ExperimentRun


__all__ = [
    "BranchExistsError",
    "BranchNotFoundError",
    "LevelNameNotFoundError",
    "LevelTypeWeirdError",
    "RunDuplicatePrimaryKeyError",
    "RunNotFoundError",
    "RunNotUniqueError",
    "RunNullColError",
    "RunUpdateArchivedError",
    "StacklevelTypeWeirdError",
    "TaskExistsError",
    "TaskNotFoundError",
    "TrackStepOutRangeError",
]


@final
class TaskExistsError(TaskCtxError, AlreadyExistsError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, task: str, branch: tuple[str, Branch] | None = None) -> None:
        if branch:
            b, ts = branch[0], tuple(t for t in branch[1]["tasks"])
            scope = f"branch '{b}' tasks: {ts}" if branch else ""
        else:
            scope = ""
        super().__init__(f"'{task}'", scope=scope)


@final
class BranchExistsError(BranchCtxError, AlreadyExistsError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, qbr: str, branches: Collection[str] | None = None) -> None:
        scope = f"branches: {tuple(branches)}" if branches else ""
        super().__init__(f"'{qbr}'", scope=scope)


@final
class TaskNotFoundError(TaskCtxError, NotFoundError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, task: str, branches: Collection[Branch] | None = None) -> None:
        if branches:
            ts = set(chain.from_iterable(b["tasks"].keys() for b in branches))
            scope = f"tasks: {tuple(sorted(ts))}"
        else:
            scope = ""
        super().__init__(f"'{task}'", scope=scope)


@final
class BranchNotFoundError(BranchCtxError, NotFoundError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, qbr: str, branches: Collection[str] | None = None) -> None:
        scope = f"branches: {tuple(branches)}" if branches else ""
        super().__init__(f"'{qbr}'", scope=scope)


@final
class LevelNameNotFoundError(LevelCtxError, NotFoundError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, lvl: str) -> None:
        super().__init__(f"'{lvl.upper()}'")


@final
class LevelTypeWeirdError(LevelCtxError, CustomTypeError, WeirdError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, lvl: object) -> None:
        super().__init__(f"'{lvl.__class__.__name__}'")


@final
class StacklevelTypeWeirdError(StacklevelCtxError, CustomTypeError, WeirdError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, stacklevel: object) -> None:
        super().__init__(f"'{stacklevel.__class__.__name__}'")


class RunNotFoundError(RunCtxError, NotFoundError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, exprun: UUID) -> None:
        super().__init__(f"'{exprun.hex}'")


@final
class RunNotUniqueError(RunCtxError, AlreadyExistsError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, exprun: ExperimentRun) -> None:
        msg = f"run (grp={exprun.grp}, exp={exprun.exp}, run={exprun.run})"
        super().__init__(msg)


@final
class RunDuplicatePrimaryKeyError(RunCtxError, AlreadyExistsError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, exprun: UUID) -> None:
        super().__init__(f"'{exprun.hex}'")


@final
class RunNullColError(RunCtxError, NullValueError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, col: str) -> None:
        super().__init__(f"'{col}'")


@final
class RunUpdateArchivedError(RunCtxError, ArchivedError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, exprun: UUID) -> None:
        super().__init__(f"'{exprun.hex}'")


@final
class TrackStepOutRangeError(TrackCtxError, StepError, OutRangeError):  # pyright: ignore[reportUnsafeMultipleInheritance]
    def __init__(self, step: int) -> None:
        super().__init__(f"{step}")
