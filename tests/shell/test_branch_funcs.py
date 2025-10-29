from sys import stderr

import pytest

from nnlogging.shell import Shell
from nnlogging.typings import BranchExistsError, BranchNotFoundError


def test_branch_add_normal(
    branch_name,
    branch_sink,
):
    shell = Shell()
    shell.branch_add(branch_name, branch_sink)
    assert branch_name in shell.branches
    branch = shell.branches[branch_name]
    assert branch["console"].file is branch_sink or stderr


def test_branch_add_duplicate(
    branch_name,
):
    shell = Shell()
    shell.branch_add(branch_name)
    with pytest.raises(BranchExistsError):
        shell.branch_add(branch_name)


def test_branch_remove_normal(
    branch_name,
):
    shell = Shell()
    shell.branch_add(branch_name)
    shell.branch_remove(branch_name)


def test_branch_remove_not_found(
    branch_name,
):
    shell = Shell()
    with pytest.raises(BranchNotFoundError):
        shell.branch_remove(branch_name)
