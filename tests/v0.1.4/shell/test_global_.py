import nnlogging
from nnlogging import Shell


def test_global_shell():
    shell = nnlogging.global_._global_shell
    assert shell.logger is None
    assert shell.run is None
    assert len(shell.branches) == 0
    assert shell.name == "_global_"


def test_replace_global_shell(
    global_shell_sink,
    global_shell_name,
):
    shell = Shell(global_shell_name)
    shell.branch_add("default", global_shell_sink)
    nnlogging.replace_global_shell(shell)
    assert nnlogging.global_._global_shell is shell
    shell.branch_remove("default")
