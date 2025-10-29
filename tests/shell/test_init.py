from nnlogging import shell as default_shell
from nnlogging.shell import Shell, ShellProtocol
from nnlogging.utils import BranchConfig, LoggerConfig, RunConfig


def test_default_shell():
    assert default_shell.logger is None
    assert default_shell.run is None
    assert default_shell.branches == dict()

    assert default_shell.name == "__nnlogging__"
    assert default_shell.logger_config == LoggerConfig(name=default_shell.name)
    assert default_shell.run_config == RunConfig()
    assert default_shell.branch_config == BranchConfig() and all(
        type(col1) == type(col2)
        for col1, col2 in zip(
            default_shell.branch_config.columns, BranchConfig().columns, strict=True
        )
    )

    assert isinstance(default_shell, ShellProtocol)


def test_shell_init(
    shell_name_gen,
    logger_name_gen,
):
    shell_name = shell_name_gen()
    logger_name = logger_name_gen()
    shell = Shell(
        shell_name,
        logger_config=LoggerConfig(name=logger_name),
    )

    assert shell.logger is None
    assert shell.run is None
    assert shell.branches == dict()

    assert shell.name == shell_name
    assert shell.logger_config == LoggerConfig(name=logger_name)
    assert shell.run_config == RunConfig()
    assert shell.branch_config == BranchConfig() and all(
        type(col1) == type(col2)
        for col1, col2 in zip(
            shell.branch_config.columns, BranchConfig().columns, strict=True
        )
    )

    assert isinstance(shell, ShellProtocol)
