from dataclasses import dataclass, field
from typing import TypedDict

from aim.storage.types import AimObject


@dataclass
class TrackOption:
    name: str | None = field(default=None)
    step: int | None = field(default=None)
    epoch: int | None = field(default=None)
    context: AimObject = field(default=None)


class TrackOptionDict(TypedDict, total=False):
    name: str | None
    step: int | None
    epoch: int | None
    context: AimObject
