import logging

from aim import Run as AimRun

from nnlogging.shell import Shell
from nnlogging.utils import BranchConfig, LoggerConfig, RunConfig, evolve_


def test_logger_configure(
    logger_config,
    logger_level_omitable,
):
    shell = Shell()
    shell.logger = logging.getLogger(shell.logger_config.name)
    shell.logger_configure(
        logger_config,
        level=logger_level_omitable,
    )
    assert shell.logger is None
    assert shell.logger_config == evolve_(
        logger_config or LoggerConfig(),
        level=logger_level_omitable,
    )


def test_run_configure(
    run_config,
    run_experiment_omitable,
    root_path,
):
    shell = Shell()
    shell.run = AimRun(repo=str(root_path))
    shell.run_configure(
        run_config or RunConfig(),
        experiment=run_experiment_omitable,
    )
    assert shell.run is None
    assert shell.run_config == evolve_(
        run_config or RunConfig(),
        experiment=run_experiment_omitable,
    )


def test_branch_configure(
    branch_config,
    branch_highlighter_omitable,
    branch_color_system_omitable,
):
    shell = Shell()
    shell.branch_configure(
        branch_config or BranchConfig(),
        highlighter=branch_highlighter_omitable,
        color_system=branch_color_system_omitable,
    )
    assert shell.branch_config == evolve_(
        branch_config or BranchConfig(),
        highlighter=branch_highlighter_omitable,
        color_system=branch_color_system_omitable,
    )
