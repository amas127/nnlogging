import logging

from aim import Run as AimRun

from nnlogging import Shell


def test_logger_configure(
    logger_level,
):
    shell = Shell()
    shell.logger = logging.getLogger(shell.logger_config.name)
    shell.logger_configure(
        level=logger_level,
    )
    assert shell.logger is None
    assert shell.logger_config.level == logger_level


def test_run_configure(
    run_experiment,
    root_path,
):
    shell = Shell()
    shell.run = AimRun(repo=str(root_path))
    shell.run_configure(
        experiment=run_experiment,
    )
    assert shell.run is None
    assert shell.run_config.experiment == run_experiment


def test_branch_configure(
    branch_highlighter,
    branch_color_system,
):
    shell = Shell()
    shell.branch_configure(
        highlighter=branch_highlighter,
        color_system=branch_color_system,
    )
    assert shell.branch_config.highlighter == branch_highlighter
    assert shell.branch_config.color_system == branch_color_system
