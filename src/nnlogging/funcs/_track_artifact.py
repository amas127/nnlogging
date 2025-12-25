import shutil
from pathlib import Path
from uuid import UUID

from nnlogging.typings import Artifact, DuckConnection, Jsonlike, StepTrack, StrPath
from nnlogging.utils import create_snapshot, digest_file, dvc_add, get_hash_prefix

from ._db import track


__all__ = ["track_artifact"]


def track_artifact(
    con: DuckConnection,
    uuid: UUID,
    *fs: StrPath,
    step: int,
    dstdir: StrPath,
    ctx: Jsonlike | None = None,
) -> None:
    dsts: list[Artifact] = []
    for f in fs:
        fsnap = create_snapshot(f)
        fhash = digest_file(fsnap, blen=16)
        shard = get_hash_prefix(fhash, blen=1)
        if not (shard_dir := Path(dstdir) / shard).exists():
            shard_dir.mkdir(parents=True, exist_ok=True)
        fdst = shutil.move(fsnap, shard_dir / fhash.hex())
        dsts.append(Artifact(path=f, storage=fdst))
    dvc_add([d["storage"] for d in dsts])
    track(con, uuid, step=step, item=StepTrack(atf=dsts, ctx=ctx))
