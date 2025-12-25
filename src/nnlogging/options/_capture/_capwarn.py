from dataclasses import dataclass, field
from typing import TypedDict

from nnlogging.typings import WarnCapturer

from .default import default_warning_capturer


__all__ = ["CapwarnFullOpt", "CapwarnParOpt"]


@dataclass(kw_only=True)
class CapwarnFullOpt:
    enabled: bool | None = field(default=None)  # NOTE: keep user space as default
    capturer: WarnCapturer = field(default_factory=default_warning_capturer)


class CapwarnParOpt(TypedDict, total=False):
    enabled: bool | None
    capturer: WarnCapturer
