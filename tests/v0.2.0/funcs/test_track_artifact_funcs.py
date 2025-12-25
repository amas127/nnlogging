from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

from nnlogging.funcs._track_artifact import track_artifact
from nnlogging.typings import StepTrack


class TestTrackArtifactFuncs:
    @patch("nnlogging.funcs._track_artifact.track")
    @patch("shutil.move")
    @patch("nnlogging.funcs._track_artifact.dvc_add")
    @patch("nnlogging.funcs._track_artifact.get_hash_prefix")
    @patch("nnlogging.funcs._track_artifact.digest_file")
    @patch("nnlogging.funcs._track_artifact.create_snapshot")
    def test_track_artifact(
        self,
        mock_create_snapshot,
        mock_digest_file,
        mock_get_hash_prefix,
        mock_dvc_add,
        mock_shutil_move,
        mock_track,
    ):
        # Setup mocks
        mock_con = MagicMock()
        mock_uuid = uuid4()
        step = 1
        dstdir = "/tmp/dst"
        ctx = {"key": "value"}
        files = ["file1.txt", "file2.txt"]

        # Mock create_snapshot to return snapshot paths
        mock_create_snapshot.side_effect = [
            "/tmp/snap1",
            "/tmp/snap2",
        ]

        # Mock digest_file to return 32 bytes hash
        mock_hash1 = b"\x00" * 32
        mock_hash2 = b"\x01" * 32
        mock_digest_file.side_effect = [mock_hash1, mock_hash2]

        # Mock get_hash_prefix to return shard strings (first 2 bytes hex, 4 chars)
        mock_get_hash_prefix.side_effect = ["0000", "0101"]

        # Mock shutil.move to return destination paths
        # 32 bytes = 64 hex characters
        mock_shutil_move.side_effect = [
            Path(dstdir) / "0000" / mock_hash1.hex(),
            Path(dstdir) / "0101" / mock_hash2.hex(),
        ]

        track_artifact(mock_con, mock_uuid, *files, step=step, dstdir=dstdir, ctx=ctx)

        # Verify create_snapshot calls
        assert mock_create_snapshot.call_count == 2
        mock_create_snapshot.assert_any_call("file1.txt")
        mock_create_snapshot.assert_any_call("file2.txt")

        # Verify digest_file calls
        assert mock_digest_file.call_count == 2
        mock_digest_file.assert_any_call("/tmp/snap1", blen=16)
        mock_digest_file.assert_any_call("/tmp/snap2", blen=16)

        # Verify get_hash_prefix calls
        assert mock_get_hash_prefix.call_count == 2
        mock_get_hash_prefix.assert_any_call(mock_hash1, blen=1)
        mock_get_hash_prefix.assert_any_call(mock_hash2, blen=1)

        # Verify shutil.move calls
        assert mock_shutil_move.call_count == 2
        expected_dst1 = Path(dstdir) / "0000" / mock_hash1.hex()
        expected_dst2 = Path(dstdir) / "0101" / mock_hash2.hex()
        mock_shutil_move.assert_any_call("/tmp/snap1", expected_dst1)
        mock_shutil_move.assert_any_call("/tmp/snap2", expected_dst2)

        # Verify dvc_add call
        mock_dvc_add.assert_called_once_with([expected_dst1, expected_dst2])

        # Verify track call
        expected_artifacts = [
            {"path": "file1.txt", "storage": str(expected_dst1)},
            {"path": "file2.txt", "storage": str(expected_dst2)},
        ]
        expected_item = StepTrack(atf=expected_artifacts, ctx=ctx)
        mock_track.assert_called_once_with(
            mock_con, mock_uuid, step=step, item=expected_item
        )
