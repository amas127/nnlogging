from dataclasses import asdict, replace

from aim.storage.types import AimObject

from nnlogging.options import RunConfigOptionDict, TrackOptionDict
from nnlogging.typings.exts import Unpack
from nnlogging.typings.protocols import ShellProtocol
from nnlogging.utils.factories import get_aim_run

__all__ = [
    "run_configure",
    "track",
    "add_tag",
    "remove_tag",
    "update_metadata",
]


def _run_open(
    inst: ShellProtocol,
):
    if inst.run is None:
        inst.run = get_aim_run(**asdict(inst.run_config))


def _run_close(
    inst: ShellProtocol,
):
    if inst.run is not None:
        inst.run.close()
        del inst.run
        inst.run = None


def run_configure(
    inst: ShellProtocol,
    **kwargs: Unpack[RunConfigOptionDict],
):
    _run_close(inst)
    inst.run_config = replace(
        inst.run_config,
        **kwargs,
    )


def track(
    inst: ShellProtocol,
    value: object,
    **kwargs: Unpack[TrackOptionDict],
):
    _run_open(inst)
    assert inst.run is not None
    inst.run.track(
        value,
        **kwargs,  # pyright: ignore[reportArgumentType]
    )


def add_tag(
    inst: ShellProtocol,
    tag: str,
):
    _run_open(inst)
    assert inst.run is not None
    inst.run.add_tag(tag)


def remove_tag(
    inst: ShellProtocol,
    tag: str,
):
    _run_open(inst)
    assert inst.run is not None
    inst.run.remove_tag(tag)


def update_metadata(
    inst: ShellProtocol,
    key: str,
    value: AimObject,
):
    _run_open(inst)
    assert inst.run is not None
    inst.run[key] = value
