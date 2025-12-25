from pathlib import Path


__all__ = ["find_storage_dir"]


def find_storage_dir(storage_dir: str) -> Path | None:
    cur_path = Path.cwd().resolve()
    home_path = Path.home().resolve()
    while cur_path:
        if (target_dir := cur_path / storage_dir).is_dir():
            return target_dir
        if cur_path in {home_path, cur_path.parent}:
            break
        cur_path = cur_path.parent
    return None
