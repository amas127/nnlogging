from __future__ import annotations

import shutil
import subprocess  # noqa: S404
import tempfile
from collections.abc import Collection
from pathlib import Path
from typing import TYPE_CHECKING

import blake3


if TYPE_CHECKING:
    from nnlogging.typings import StrPath


__all__ = ["create_snapshot", "digest_file", "dvc_add", "get_hash_prefix"]


def create_snapshot(src: StrPath, dst: StrPath | None = None) -> Path:
    if dst is None:
        # `NamedTemporaryFile` can be recycled when closed but file remained
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix="nnlogging_snapshot_", delete=False
        ) as temp:
            # `shutil.copy2` keeps metadata while maintaining portable
            dstfile = shutil.copy2(src, temp.name, follow_symlinks=True)
    else:
        # `shutil.copy2` allows to copy to a directory and return actual path
        # file will be overwritten if names collide
        dstfile = shutil.copy2(src, dst, follow_symlinks=True)
    return Path(dstfile)


def digest_file(f: StrPath, blen: int) -> bytes:
    if not Path(f).stat().st_size:
        raise LookupError
    hasher = blake3.blake3()
    return hasher.update_mmap(f).digest(blen)


def get_hash_prefix(h: bytes, blen: int) -> str:
    return h[:blen].hex() if blen < len(h) else h.hex()


def dvc_add(file: StrPath | Collection[StrPath]) -> None:
    if not file:
        raise ValueError
    if not (dvcexe := shutil.which("dvc")):
        raise LookupError
    parcmd = [dvcexe, "add", "--quiet"]
    # MAYBE: decide throw error type when failed
    match file:
        case str() | Path():
            _ = subprocess.run([*parcmd, str(file)], check=True)  # noqa: S603, pyright: ignore[reportCallIssue]
        case Collection():
            _ = subprocess.run([*parcmd, *(str(f) for f in file)], check=True)  # noqa: S603, pyright: ignore[reportCallIssue]
        case _:
            raise TypeError
