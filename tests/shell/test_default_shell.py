import nnlogging
from nnlogging import Shell, get_default_shell, replace_default_shell
from nnlogging.shell_protocol import ShellProtocol
from nnlogging.utils import BranchConfig, LoggerConfig, RunConfig


def test_get_default_shell(
    default_shell_sink,
    default_shell_logger_name,
):
    nnlogging.shell.default_shell = None
    default_shell = get_default_shell(default_shell_sink)
    default_shell.logger_configure(name=default_shell_logger_name)

    assert default_shell.logger is None
    assert default_shell.run is None
    assert "default" in default_shell.branches
    assert default_shell.branches["default"]["console"].file == default_shell_sink

    assert default_shell.name == "nnlogging"
    assert default_shell.logger_config == LoggerConfig(name=default_shell_logger_name)
    assert default_shell.run_config == RunConfig()
    assert default_shell.branch_config == BranchConfig() and all(
        type(col1) == type(col2)
        for col1, col2 in zip(
            default_shell.branch_config.columns, BranchConfig().columns, strict=True
        )
    )

    assert isinstance(default_shell, ShellProtocol)


def test_replace_default_shell():
    nnlogging.shell.default_shell = None
    _ = get_default_shell()
    assert isinstance(nnlogging.shell.default_shell, Shell)
    new_shell = Shell()
    replace_default_shell(new_shell)
    assert nnlogging.shell.default_shell is new_shell


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
