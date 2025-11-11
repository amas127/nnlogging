import sys
from dataclasses import asdict, replace
from typing import Literal, cast

from nnlogging.exceptions import (
    call_branch_exists_error,
    call_branch_not_found_error,
)
from nnlogging.options import BranchConfigOptionDict
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ShellProtocol, Sink
from nnlogging.utils.factories import get_branch

__all__ = [
    "branch_configure",
    "branch_add",
    "branch_remove",
]


def branch_configure(
    inst: ShellProtocol,
    **kwargs: Unpack[BranchConfigOptionDict],
):
    inst.branch_config = replace(
        inst.branch_config,
        **kwargs,
    )


def branch_add(
    inst: ShellProtocol,
    name: str,
    sink: Sink | Literal["stderr", "stdout"] = "stderr",
    **kwargs: Unpack[BranchConfigOptionDict],
):
    if name in inst.branches:
        e = call_branch_exists_error(
            inst,
            name,
            stacklevel=2,
        )
        if inst.strict:
            raise e

    else:
        if isinstance(sink, str) and sink in ("stderr", "stdout"):
            sink = cast(Sink, getattr(sys, sink))
        branch = get_branch(
            sink,
            **(asdict(inst.branch_config) | kwargs),  # pyright: ignore[reportArgumentType]
        )
        inst.branches[name] = branch
        if inst.logger is not None:
            inst.logger.addHandler(branch["handler"])


def branch_remove(
    inst: ShellProtocol,
    name: str,
):
    if name not in inst.branches:
        e = call_branch_not_found_error(
            inst,
            name,
            stacklevel=2,
        )
        if inst.strict:
            raise e

    else:
        branch = inst.branches[name]
        branch["handler"].close()
        branch["tasks"].clear()
        if branch["progress"] is not None:
            branch["progress"].stop()
        if inst.logger is not None:
            inst.logger.removeHandler(branch["handler"])
        del inst.branches[name]
