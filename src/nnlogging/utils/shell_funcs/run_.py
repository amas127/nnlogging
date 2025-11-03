from aim import Repo as AimRepo
from aim.sdk.types import AimObject

from nnlogging.shell_protocol import ShellProtocol
from nnlogging.typings import Omitable
from nnlogging.utils.factory_funcs.shell_ import RunConfig, get_aim_run
from nnlogging.utils.helpers import evolve_


def _run_open(
    inst: ShellProtocol,
    /,
):
    if inst.run is None:
        inst.run = get_aim_run(inst.run_config)


def _run_close(
    inst: ShellProtocol,
    /,
):
    if inst.run is not None:
        inst.run.close()
        del inst.run
        inst.run = None


def run_configure(
    inst: ShellProtocol,
    /,
    config: RunConfig | None = None,
    *,
    experiment: Omitable[str | None] = ...,
    repo: Omitable[str | AimRepo | None] = ...,
    system_tracking_interval: Omitable[float | None] = ...,
    capture_terminal_logs: Omitable[bool] = ...,
    log_system_params: Omitable[bool] = ...,
    run_hash: Omitable[str | None] = ...,
    read_only: Omitable[bool] = ...,
    force_resume: Omitable[bool] = ...,
):
    _run_close(inst)
    inst.run_config = evolve_(
        config or inst.run_config,
        experiment=experiment,
        repo=repo,
        system_tracking_interval=system_tracking_interval,
        capture_terminal_logs=capture_terminal_logs,
        log_system_params=log_system_params,
        run_hash=run_hash,
        read_only=read_only,
        force_resume=force_resume,
    )


def update_metadata(
    inst: ShellProtocol,
    /,
    label: str,
    metadata: AimObject,
):
    _run_open(inst)
    assert inst.run is not None
    inst.run[label] = metadata


def add_tag(inst: ShellProtocol, /, tag: str):
    _run_open(inst)
    assert inst.run is not None
    inst.run.add_tag(tag)


def remove_tag(inst: ShellProtocol, /, tag: str):
    _run_open(inst)
    assert inst.run is not None
    inst.run.remove_tag(tag)


def track(
    inst: ShellProtocol,
    /,
    value: object,
    *,
    name: str | None = None,
    step: int | None = None,
    epoch: int | None = None,
    context: AimObject = None,
):
    _run_open(inst)
    assert inst.run is not None
    inst.run.track(
        value,
        name=name,  # pyright: ignore[reportArgumentType]
        step=step,  # pyright: ignore[reportArgumentType]
        epoch=epoch,  # pyright: ignore[reportArgumentType]
        context=context,
    )
