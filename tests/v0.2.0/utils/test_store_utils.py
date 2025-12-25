import shutil
import string
import subprocess
from pathlib import Path
from unittest.mock import patch

import blake3
import pytest

from nnlogging.utils import create_snapshot, digest_file, dvc_add, get_hash_prefix


@pytest.fixture
def temp_dir():
    dir = Path("pytest_cache")
    try:
        dir.mkdir(exist_ok=True)
        yield str(dir.resolve())
    finally:
        shutil.rmtree(dir)


@pytest.fixture
def dummy_file(temp_dir):
    dir = Path(temp_dir)
    f = dir / "dummy_file.txt"
    try:
        f.touch()
        yield f
    finally:
        Path(f).unlink()


@pytest.fixture
def dummy_files(temp_dir):
    dir = Path(temp_dir)
    files = {}

    try:
        files["small"] = dir / "small.txt"
        files["small"].write_text("small file content")

        files["medium"] = dir / "medium.txt"
        files["medium"].write_bytes(b"x" * 1024 * 10)  # 10KB

        files["large"] = dir / "large.txt"
        files["large"].write_bytes(b"y" * 1024 * 1024)  # 1MB

        files["empty"] = dir / "empty.txt"
        files["empty"].touch()

        files["special"] = dir / "special_chars.txt"
        files["special"].write_text("file with\nnewlines\tand tabs")

        yield files
    finally:
        for f in files.values():
            Path(f).unlink()


@pytest.fixture
def empty_file(temp_dir):
    dir = Path(temp_dir)
    f = dir / "emptyfile"
    try:
        f.touch(exist_ok=True)
        yield str(f.resolve())
    finally:
        Path(f).unlink()


@pytest.fixture
def large_file(temp_dir):
    dir = Path(temp_dir)
    f = dir / "largefile"
    try:
        f.touch(exist_ok=True)
        with f.open("wb") as b:
            b.write(b"x" * 1024 * 1024)
        yield str(f.resolve())
    finally:
        Path(f).unlink()


@pytest.fixture
def temp_file(temp_dir):
    dir = Path(temp_dir)
    f = dir / "tempfile"
    try:
        f.touch(exist_ok=True)
        with f.open("wb") as b:
            b.write(b"hello world")
        yield str(f.resolve())
    finally:
        Path(f).unlink()


@pytest.fixture
def mock_which_dvc():
    with patch("shutil.which") as mock_which:
        mock_which.return_value = "dvc"
        yield mock_which


class TestCreateSnapshot:
    def test_create_snapshot_without_dst(self, temp_file):
        """Test creating snapshot without destination (uses temp file)."""
        result = create_snapshot(temp_file)
        assert isinstance(result, Path)
        assert result.exists()
        assert result.read_bytes() == b"hello world"
        result.unlink()

    def test_create_snapshot_with_dst_file(self, temp_file, temp_dir):
        dst_path = Path(temp_dir) / "snapshot_copy"
        result = create_snapshot(temp_file, dst_path)
        assert result == dst_path
        assert dst_path.exists()
        assert dst_path.read_bytes() == b"hello world"

    def test_create_snapshot_with_dst_dir(self, temp_file, tmp_path):
        result = create_snapshot(temp_file, tmp_path)
        assert result.parent == Path(tmp_path)
        assert result.exists()
        assert result.read_bytes() == b"hello world"

    def test_create_snapshot_nonexistent_src(self):
        with pytest.raises(FileNotFoundError):
            create_snapshot("nonexistent_file.txt")

    def test_create_snapshot_preserves_metadata(self, temp_file):
        Path(temp_file).chmod(0o644)
        stat_before = Path(temp_file).stat()
        result = create_snapshot(temp_file)
        try:
            stat_after = result.stat()
            assert abs(stat_after.st_mtime - stat_before.st_mtime) < 0.001
        finally:
            result.unlink()

    def test_create_snapshot_with_large_file(self, large_file):
        result = create_snapshot(large_file)
        assert isinstance(result, Path)
        assert result.exists()
        assert result.stat().st_size == 1024 * 1024
        result.unlink()


class TestDigestFile:
    def test_digest_file_normal(self, temp_file):
        result = digest_file(temp_file, 32)
        assert isinstance(result, bytes)
        assert len(result) == 32
        # Verify it's a valid BLAKE3 hash
        expected = blake3.blake3().update(b"hello world").digest(32)
        assert result == expected

    @pytest.mark.parametrize("blen", [16, 32, 64, 128])
    def test_digest_file_different_lengths(self, temp_file, blen):
        result = digest_file(temp_file, blen)
        assert isinstance(result, bytes)
        assert len(result) == blen

    def test_digest_file_empty_file(self, empty_file):
        with pytest.raises(LookupError):
            digest_file(empty_file, 32)

    def test_digest_file_nonexistent(self):
        with pytest.raises(FileNotFoundError):
            digest_file("nonexistent.txt", 32)

    def test_digest_file_large_file(self, large_file):
        result = digest_file(large_file, 32)
        assert isinstance(result, bytes)
        assert len(result) == 32
        result2 = digest_file(large_file, 32)
        assert result == result2

    def test_digest_file_memory_mapped(self, temp_file):
        result = digest_file(temp_file, 32)
        assert isinstance(result, bytes)
        assert len(result) == 32


class TestGetHashPrefix:
    def test_get_hash_prefix_normal(self):
        test_hash = b"0123456789abcdef" * 4  # 64 bytes
        result = get_hash_prefix(test_hash, 2)
        assert isinstance(result, str)
        assert result == "3031"

    @pytest.mark.parametrize(
        ("x", "y"),
        [
            (0, ""),
            (1, "30"),
            (2, "3031"),
            (4, "30313233"),
            (8, "3031323334353637"),
            (16, "30313233343536373839616263646566"),
        ],
    )
    def test_get_hash_prefix_various_lengths(self, x, y):
        test_hash = b"0123456789abcdef" * 4  # 64 bytes
        result = get_hash_prefix(test_hash, x)
        assert result == y

    def test_get_hash_prefix_length_exceeds_hash(self):
        test_hash = b"01234567"
        result = get_hash_prefix(test_hash, 10)
        assert result == test_hash.hex()

    def test_get_hash_prefix_hex_encoding(self):
        test_hash = b"test hash data"
        result = get_hash_prefix(test_hash, 10)
        assert all(c in string.hexdigits for c in result)


class TestDvcAdd:
    def test_dvc_add_single_file(self, temp_file, mock_which_dvc):
        with patch("subprocess.run") as mock_run:
            dvc_add(temp_file)
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == mock_which_dvc()
            assert args[1] == "add"
            assert args[2] == "--quiet"
            assert args[3] == temp_file

    def test_dvc_add_multiple_files(self, temp_dir):
        file1 = Path(temp_dir) / "file1.txt"
        file2 = Path(temp_dir) / "file2.txt"
        file1.write_text("test1")
        file2.write_text("test2")

        with patch("shutil.which") as mock_which, patch("subprocess.run") as mock_run:
            mock_which.return_value = "dvc"
            dvc_add([file1, file2])
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert args[0] == "dvc"
            assert args[1] == "add"
            assert args[2] == "--quiet"
            assert str(file1) in args
            assert str(file2) in args

    def test_dvc_add_path_object(self, temp_file):
        with patch("subprocess.run") as mock_run:
            dvc_add(Path(temp_file))
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            assert str(Path(temp_file)) in args

    def test_dvc_add_dvc_not_found(self, temp_file):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = None
            with pytest.raises(LookupError):
                dvc_add(temp_file)

    def test_dvc_add_invalid_input_type(self):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = "/usr/bin/dvc"
            with pytest.raises(TypeError):
                dvc_add(123)  # type: ignore[arg-type]

    def test_dvc_add_subprocess_error(self, temp_file):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
            with pytest.raises(subprocess.CalledProcessError):
                dvc_add(temp_file)


class TestScalability:
    @pytest.mark.parametrize("sz", [1, 1024, 1024 * 1024])
    def test_digest_file_with_various_sizes(self, temp_dir, sz):
        test_file = Path(temp_dir) / f"test_{sz}.dat"
        test_file.write_bytes(b"x" * sz)

        digest = digest_file(test_file, 32)
        assert len(digest) == 32

    def test_create_snapshot_multiple_files(self, temp_dir):
        file_count = 100
        files = []

        # Create many files
        for i in range(file_count):
            test_file = Path(temp_dir) / f"test_{i}.txt"
            test_file.write_text(f"content {i}")
            files.append(test_file)

        # Create snapshots of all files
        snapshots = []
        for file in files:
            snapshot = create_snapshot(file, Path(temp_dir) / "snapshots")
            snapshots.append(snapshot)
            assert snapshot.exists()

        assert len(snapshots) == file_count

    def test_get_hash_prefix_consistency(self):
        test_data = b"test data for hash consistency"
        prefix_length = 4

        results = []
        for _ in range(100):
            prefix = get_hash_prefix(test_data, prefix_length)
            results.append(prefix)

        assert len(set(results)) == 1


class TestReadDvcAdd:
    def test_dvc_add_single_file_integration(self, dummy_file):
        dvc_file = Path(str(dummy_file) + ".dvc")
        with dummy_file.open("w+", encoding="utf-8") as f:
            f.write("This is a test file.")
            dvc_add(str(dummy_file))
            assert dvc_file.exists()
            assert dvc_file.stat().st_size > 0

    def test_dvc_add_nonexist(self):
        name = Path("nonexist")
        with pytest.raises(subprocess.CalledProcessError):
            dvc_add(name.name)


class TestDvcAddMultiFileIntegration:
    """Comprehensive multi-file DVC integration tests with real DVC operations."""

    def test_dvc_add_multiple_files_real(self, dummy_files):
        """Test basic multi-file DVC add functionality with real commands."""
        # Get list of test files to add
        files_to_add = [
            dummy_files["small"],
            dummy_files["medium"],
            dummy_files["large"],
        ]

        # Call dvc_add with multiple files
        dvc_add(files_to_add)

        # Verify .dvc files are created for each file
        for file_path in files_to_add:
            dvc_file = Path(str(file_path) + ".dvc")
            assert dvc_file.exists(), f"DVC file not created for {file_path}"
            assert dvc_file.stat().st_size > 0, f"DVC file is empty for {file_path}"

    def test_dvc_add_empty_collection(self):
        """Test empty collection handling."""
        with pytest.raises(ValueError):
            dvc_add([])

    def test_dvc_add_mixed_valid_invalid(self, dummy_files):
        """Test partial file failures."""
        # Mix of valid and invalid file paths
        valid_file = dummy_files["small"]
        invalid_file = Path("pytest_cache") / "nonexistent.txt"

        files_to_add = [valid_file, invalid_file]

        # Should raise CalledProcessError due to invalid file
        with pytest.raises(subprocess.CalledProcessError):
            dvc_add(files_to_add)

    def test_dvc_add_duplicate_files(self, dummy_files):
        """Test duplicate file handling."""
        valid_file = dummy_files["small"]

        # Add same file multiple times in the collection
        files_to_add = [valid_file, valid_file, valid_file]

        # This should work without error (DVC handles duplicates gracefully)
        dvc_add(files_to_add)

        # Only one .dvc file should be created
        dvc_file = Path(str(valid_file) + ".dvc")
        assert dvc_file.exists()

    def test_dvc_add_symlinks(self, dummy_files):
        """Test symlink behavior."""
        target_file = dummy_files["small"]
        symlink_file = Path("pytest_cache") / "symlink.txt"

        # Create symlink
        symlink_file.symlink_to(target_file.resolve())

        # Add symlink
        dvc_add([symlink_file])

        # Verify .dvc file is created for symlink
        dvc_file = Path(str(symlink_file) + ".dvc")
        assert dvc_file.exists()

    def test_dvc_add_large_files(self, dummy_files):
        """Test large file handling."""
        large_file = dummy_files["large"]

        # Add large file
        dvc_add(large_file)

        # Verify .dvc file is created
        dvc_file = Path(str(large_file) + ".dvc")
        assert dvc_file.exists()

        # Verify cache contains file content
        result = subprocess.run(
            ["dvc", "status"], capture_output=True, text=True, check=True
        )
        assert str(large_file.name) not in result.stdout
