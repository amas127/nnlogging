from dataclasses import dataclass, field
from typing import TypedDict

from aim import Repo as AimRepo


@dataclass(kw_only=True)
class RunConfigOption:
    experiment: str | None = field(default=None)
    repo: str | AimRepo | None = field(default=None)
    system_tracking_interval: float | None = field(default=10)
    capture_terminal_logs: bool = field(default=False)
    log_system_params: bool = field(default=False)
    run_hash: str | None = field(default=None)
    read_only: bool = field(default=False)
    force_resume: bool = field(default=False)


class RunConfigOptionDict(TypedDict, total=False):
    experiment: str | None
    repo: str | AimRepo | None
    system_tracking_interval: float | None
    capture_terminal_logs: bool
    log_system_params: bool
    run_hash: str | None
    read_only: bool
    force_resume: bool
