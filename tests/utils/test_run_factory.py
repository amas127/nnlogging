from nnlogging.utils import RunConfig, evolve_, get_aim_run


def test_get_aim_run(
    root_path,
    run_config,
    run_experiment_omitable,
):
    run = get_aim_run(
        run_config,
        experiment=run_experiment_omitable,
        repo=str(root_path),
    )
    target_config = evolve_(
        run_config or RunConfig(),
        experiment=run_experiment_omitable,
        repo=str(root_path),
    )
    assert run.experiment == target_config.experiment or "default"
    assert run.repo.path == str(root_path / ".aim")
