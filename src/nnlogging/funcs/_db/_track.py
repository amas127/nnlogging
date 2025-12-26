from functools import lru_cache
from pathlib import Path
from uuid import UUID

from duckdb import ConversionException

from nnlogging.exceptions import TrackStepOutRangeError
from nnlogging.helpers import dumps
from nnlogging.typings import DuckConnection, StepTrack
from nnlogging.utils import check_exprun_updatable


__all__ = ["track"]


@lru_cache
def _sqlstr_track() -> str:
    with Path(__file__).parent.joinpath("track.sql").open("r") as f:
        return f.read()


def track(
    con: DuckConnection,
    uuid: UUID,
    *,
    step: int,
    item: StepTrack,
) -> None:
    if check_exprun_updatable(con, uuid):
        met = dumps(item.met)
        atf = dumps(item.atf)
        ctx = dumps(item.ctx)
        try:
            _ = con.execute(_sqlstr_track(), (uuid, step, met, atf, ctx))
        except ConversionException as e:
            emsg = str(e)
            if "out of range" in emsg:
                raise TrackStepOutRangeError(step) from e
            raise  # pragma: no cover
