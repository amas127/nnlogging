import time
from unittest.mock import Mock, patch
from uuid import UUID

import pytest

from nnlogging.exceptions import (
    BranchExistsError,
    BranchNotFoundError,
    RunNotFoundError,
    RunUpdateArchivedError,
    TaskExistsError,
    TaskNotFoundError,
)
from nnlogging.utils import (
    check_branch_found,
    check_branch_not_exists,
    check_exprun_updatable,
    check_task_found,
    check_task_not_exists,
)
from nnlogging.utils._check import _sqlstr_select_archived


# Type aliases for test data
TEST_BRANCHES = dict[str, dict]  # Simplified type for testing


class TestCheckTaskNotExists:
    """Test check_task_not_exists function with all branch flows."""

    def test_task_not_exists_returns_true(self):
        """Test that function returns True when task doesn't exist."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        result = check_task_not_exists(branches, "task3")
        assert result is True

    def test_task_exists_raises_exception(self):
        """Test that function raises TaskExistsError when task exists."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        with pytest.raises(TaskExistsError) as exc_info:
            check_task_not_exists(branches, "task1")
        assert "task1" in str(exc_info.value)

    def test_task_exists_no_exception_returns_false(self):
        """Test that function returns False when task exists and exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        result = check_task_not_exists(branches, "task1", exc_raise=False)
        assert result is False

    def test_task_exists_with_callback(self):
        """Test that callback is called with proper formatting when task exists."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        with pytest.raises(TaskExistsError):
            check_task_not_exists(branches, "task1", exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Task '%s' already exists in branch '%s'"
        assert call_args[0][1] == "task1"
        assert call_args[0][2] == "branch1"

    def test_task_exists_no_exception_with_callback(self):
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        result = check_task_not_exists(
            branches, "task1", exc_raise=False, exc_callback=callback_mock
        )
        assert result is False
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Task '%s' already exists in branch '%s'"
        assert call_args[0][1] == "task1"
        assert call_args[0][2] == "branch1"

    def test_task_exists_in_multiple_branches(self):
        """Test behavior when task exists in multiple branches."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task1": {}}},
        }
        with pytest.raises(TaskExistsError) as exc_info:
            check_task_not_exists(branches, "task1")
        assert "task1" in str(exc_info.value)

    def test_empty_branches_dict(self):
        """Test behavior with empty branches dictionary."""
        branches = {}
        result = check_task_not_exists(branches, "task1")
        assert result is True

    def test_branch_with_empty_tasks(self):
        """Test behavior when branch has empty tasks dictionary."""
        branches = {"branch1": {"tasks": {}}, "branch2": {"tasks": {"task2": {}}}}
        result = check_task_not_exists(branches, "task1")
        assert result is True


class TestCheckTaskFound:
    """Test check_task_found function with all branch flows."""

    def test_task_found_returns_true(self):
        """Test that function returns True when task is found."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        result = check_task_found(branches, "task1")
        assert result is True

    def test_task_not_found_raises_exception(self):
        """Test that function raises TaskNotFoundError when task not found."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        with pytest.raises(TaskNotFoundError) as exc_info:
            check_task_found(branches, "task3")
        assert "task3" in str(exc_info.value)

    def test_task_not_found_no_exception_returns_false(self):
        """Test that function returns False when task not found and exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        result = check_task_found(branches, "task2", exc_raise=False)
        assert result is False

    def test_task_not_found_with_callback(self):
        """Test that callback is called with proper formatting when task not found."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        with pytest.raises(TaskNotFoundError):
            check_task_found(branches, "task2", exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Task '%s' not found in branches"
        assert call_args[0][1] == "task2"
        # Verify the formatted message would be: "Task 'task2' not found in branches"

    def test_task_not_found_no_exception_with_callback(self):
        """Test callback behavior with formatting when exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        result = check_task_found(
            branches, "task2", exc_raise=False, exc_callback=callback_mock
        )
        assert result is False
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Task '%s' not found in branches"
        assert call_args[0][1] == "task2"

    def test_task_found_in_multiple_branches(self):
        """Test behavior when task exists in multiple branches."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task1": {}}},
        }
        result = check_task_found(branches, "task1")
        assert result is True

    def test_empty_branches_dict_task_not_found(self):
        """Test behavior with empty branches dictionary."""
        branches = {}
        with pytest.raises(TaskNotFoundError):
            _ = check_task_found(branches, "task1")

    def test_branch_with_empty_tasks_task_not_found(self):
        """Test behavior when branch has empty tasks dictionary."""
        branches = {"branch1": {"tasks": {}}, "branch2": {"tasks": {"task2": {}}}}
        with pytest.raises(TaskNotFoundError):
            _ = check_task_found(branches, "task1")


class TestCheckBranchNotExists:
    """Test check_branch_not_exists function with all branch flows."""

    def test_branch_not_exists_returns_true(self):
        """Test that function returns True when branch doesn't exist."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        result = check_branch_not_exists(branches, "branch3")
        assert result is True

    def test_branch_exists_raises_exception(self):
        """Test that function raises BranchExistsError when branch exists."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        with pytest.raises(BranchExistsError) as exc_info:
            check_branch_not_exists(branches, "branch1")
        assert "branch1" in str(exc_info.value)

    def test_branch_exists_no_exception_returns_false(self):
        """Test that function returns False when branch exists and exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        result = check_branch_not_exists(branches, "branch1", exc_raise=False)
        assert result is False

    def test_branch_exists_with_callback(self):
        """Test that callback is called with proper formatting when branch exists."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        with pytest.raises(BranchExistsError):
            check_branch_not_exists(branches, "branch1", exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Branch '%s' already exists in branches"
        assert call_args[0][1] == "branch1"
        # Verify the formatted message would be: "Branch 'branch1' already exists in branches"

    def test_branch_exists_no_exception_with_callback(self):
        """Test callback behavior with formatting when exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        result = check_branch_not_exists(
            branches, "branch1", exc_raise=False, exc_callback=callback_mock
        )
        assert result is False
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Branch '%s' already exists in branches"
        assert call_args[0][1] == "branch1"

    def test_empty_branches_dict(self):
        """Test behavior with empty branches dictionary."""
        branches = {}
        result = check_branch_not_exists(branches, "branch1")
        assert result is True


class TestCheckBranchFound:
    """Test check_branch_found function with all branch flows."""

    def test_branch_found_returns_true(self):
        """Test that function returns True when branch is found."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        result = check_branch_found(branches, "branch1")
        assert result is True

    def test_branch_not_found_raises_exception(self):
        """Test that function raises BranchNotFoundError when branch not found."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task2": {}}},
        }
        with pytest.raises(BranchNotFoundError) as exc_info:
            check_branch_found(branches, "branch3")
        assert "branch3" in str(exc_info.value)

    def test_branch_not_found_no_exception_returns_false(self):
        """Test that function returns False when branch not found and exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        result = check_branch_found(branches, "branch2", exc_raise=False)
        assert result is False

    def test_branch_not_found_with_callback(self):
        """Test that callback is called with proper formatting when branch not found."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        with pytest.raises(BranchNotFoundError):
            check_branch_found(branches, "branch2", exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Branch '%s' not found in branches"
        assert call_args[0][1] == "branch2"
        # Verify the formatted message would be: "Branch 'branch2' not found in branches"

    def test_branch_not_found_no_exception_with_callback(self):
        """Test callback behavior with formatting when exc_raise=False."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()
        result = check_branch_found(
            branches, "branch2", exc_raise=False, exc_callback=callback_mock
        )
        assert result is False
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Branch '%s' not found in branches"
        assert call_args[0][1] == "branch2"

    def test_empty_branches_dict_branch_not_found(self):
        """Test behavior with empty branches dictionary."""
        branches = {}
        with pytest.raises(BranchNotFoundError):
            _ = check_branch_found(branches, "branch1")


class TestCheckExpRunUpdatable:
    """Test check_exprun_updatable function with all branch flows."""

    def test_run_updatable_returns_true(self):
        """Test that function returns True when run exists and is not archived."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = [(False,)]
        uuid = UUID("12345678-1234-5678-1234-567812345678")

        result = check_exprun_updatable(mock_con, uuid)
        assert result is True
        mock_con.execute.assert_called_once()

    def test_run_not_found_raises_exception(self):
        """Test that function raises RunNotFoundError when run doesn't exist."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = []
        uuid = UUID("12345678-1234-5678-1234-567812345678")

        with pytest.raises(RunNotFoundError) as exc_info:
            check_exprun_updatable(mock_con, uuid)
        assert uuid.hex in str(exc_info.value)

    def test_run_archived_raises_exception(self):
        """Test that function raises RunUpdateArchivedError when run is archived."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = [(True,)]
        uuid = UUID("12345678-1234-5678-1234-567812345678")

        with pytest.raises(RunUpdateArchivedError) as exc_info:
            check_exprun_updatable(mock_con, uuid)
        assert uuid.hex in str(exc_info.value)

    def test_run_not_found_no_exception_returns_false(self):
        """Test that function returns False when run not found and exc_raise=False."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = []
        uuid = UUID("12345678-1234-5678-1234-567812345678")

        result = check_exprun_updatable(mock_con, uuid, exc_raise=False)
        assert result is False

    def test_run_archived_no_exception_returns_false(self):
        """Test that function returns False when run archived and exc_raise=False."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = [(True,)]
        uuid = UUID("12345678-1234-5678-1234-567812345678")

        result = check_exprun_updatable(mock_con, uuid, exc_raise=False)
        assert result is False

    def test_run_not_found_with_callback(self):
        """Test that callback is called with proper formatting when run not found."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = []
        uuid = UUID("12345678-1234-5678-1234-567812345678")
        callback_mock = Mock()

        with pytest.raises(RunNotFoundError):
            check_exprun_updatable(mock_con, uuid, exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Run '%s' cannot be updated"
        assert call_args[0][1] == uuid.hex
        # Verify the formatted message would be: "Run '12345678123456781234567812345678' cannot be updated"

    def test_run_archived_with_callback(self):
        """Test that callback is called with proper formatting when run is archived."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = [(True,)]
        uuid = UUID("12345678-1234-5678-1234-567812345678")
        callback_mock = Mock()

        with pytest.raises(RunUpdateArchivedError):
            check_exprun_updatable(mock_con, uuid, exc_callback=callback_mock)
        callback_mock.assert_called_once()
        # Verify format string and arguments
        call_args = callback_mock.call_args
        assert call_args[0][0] == "Run '%s' cannot be updated"
        assert call_args[0][1] == uuid.hex
        # Verify the formatted message would be: "Run '12345678123456781234567812345678' cannot be updated"


class TestEdgeCases:
    """Test edge cases and scalability considerations."""

    def test_empty_branches_dict(self):
        """Test behavior with empty branches dictionary."""
        branches = {}

        # Task checks
        assert check_task_not_exists(branches, "task1") is True
        assert check_task_found(branches, "task1", exc_raise=False) is False

        # Branch checks
        assert check_branch_not_exists(branches, "branch1") is True
        assert check_branch_found(branches, "branch1", exc_raise=False) is False

    def test_empty_tasks_dict(self):
        """Test behavior when branch has empty tasks dictionary."""
        branches = {"branch1": {"tasks": {}}, "branch2": {"tasks": {"task2": {}}}}

        # Task should not exist in empty tasks dict
        assert check_task_not_exists(branches, "task1") is True
        assert check_task_found(branches, "task1", exc_raise=False) is False

        # Task should exist in non-empty tasks dict
        assert check_task_not_exists(branches, "task2", exc_raise=False) is False
        assert check_task_found(branches, "task2") is True

    def test_multiple_branches_same_task(self):
        """Test behavior when task exists in multiple branches."""
        branches = {
            "branch1": {"tasks": {"task1": {}}},
            "branch2": {"tasks": {"task1": {}}},
            "branch3": {"tasks": {"task2": {}}},
        }

        # Task exists in multiple branches
        with pytest.raises(TaskExistsError):
            check_task_not_exists(branches, "task1")
        assert check_task_found(branches, "task1") is True

    def test_large_branches_dict_performance(self):
        """Test performance with large branches dictionary."""

        # Create large branches dict
        branches = {}
        for i in range(1000):
            branches[f"branch{i}"] = {"tasks": {f"task{i}": {}}}

        # Test finding a task at the end
        start_time = time.time()
        result = check_task_found(branches, "task999")
        end_time = time.time()

        assert result is True
        # Should complete quickly (less than 100ms for 1000 branches)
        assert end_time - start_time < 0.1

    def test_none_uuid_handling(self):
        """Test error handling for None UUID in check_exprun_updatable."""
        mock_con = Mock()
        mock_con.execute.return_value.fetchall.return_value = []

        # This should raise an error when trying to access .hex on None
        with pytest.raises(AttributeError):
            check_exprun_updatable(mock_con, None)  # type: ignore

    def test_malformed_branches_structure(self):
        """Test error handling for malformed branches structure."""
        branches = {
            "branch1": {"tasks": "not_a_dict"},  # Invalid structure
            "branch2": {"tasks": {"task2": {}}},
        }

        # Should handle gracefully or raise appropriate error
        with pytest.raises(AttributeError):
            check_task_found(branches, "task1")


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_multiple_checks_workflow(self):
        """Test typical workflow using multiple check functions."""
        branches = {}

        # 1. Check branch doesn't exist, then add it
        assert check_branch_not_exists(branches, "experiment1") is True
        branches["experiment1"] = {"tasks": {}}
        assert check_branch_found(branches, "experiment1") is True

        # 2. Check task doesn't exist in branch, then add it
        assert check_task_not_exists(branches, "train") is True
        branches["experiment1"]["tasks"]["train"] = {}
        assert check_task_found(branches, "train") is True

        # 3. Try to add duplicate branch
        assert (
            check_branch_not_exists(branches, "experiment1", exc_raise=False) is False
        )

        # 4. Try to add duplicate task
        assert check_task_not_exists(branches, "train", exc_raise=False) is False

    def test_error_propagation_with_callbacks(self):
        """Test that errors are properly propagated through callback chain."""
        branches = {"branch1": {"tasks": {"task1": {}}}}
        callback_mock = Mock()

        # Test task exists callback
        with pytest.raises(TaskExistsError):
            check_task_not_exists(branches, "task1", exc_callback=callback_mock)
        callback_mock.assert_called_once()

        # Reset mock and test task not found callback
        callback_mock.reset_mock()
        with pytest.raises(TaskNotFoundError):
            check_task_found(branches, "task2", exc_callback=callback_mock)
        callback_mock.assert_called_once()

    def test_mixed_exception_modes(self):
        """Test mixing exc_raise=True and exc_raise=False in same workflow."""
        branches = {"branch1": {"tasks": {"task1": {}}}}

        # First check with exception raising
        with pytest.raises(TaskExistsError):
            check_task_not_exists(branches, "task1", exc_raise=True)

        # Second check without exception raising
        result = check_task_not_exists(branches, "task1", exc_raise=False)
        assert result is False

        # Third check with exception raising again
        with pytest.raises(TaskNotFoundError):
            check_task_found(branches, "task2", exc_raise=True)


class TestPerformance:
    """Performance and scalability tests."""

    def test_large_dataset_performance(self):
        """Test performance with 10,000+ branches."""

        # Create large dataset
        branches = {}
        for i in range(10000):
            branches[f"branch{i}"] = {"tasks": {f"task{i}": {}}}

        # Test worst-case scenario (task at end)
        start_time = time.time()
        result = check_task_found(branches, "task9999")
        end_time = time.time()

        assert result is True
        # Should complete in reasonable time (less than 1 second for 10k branches)
        assert end_time - start_time < 1.0

        # Test best-case scenario (task at beginning)
        start_time = time.time()
        result = check_task_found(branches, "task0")
        end_time = time.time()

        assert result is True
        # Should be very fast for first item
        assert end_time - start_time < 0.01

    def test_caching_effectiveness(self):
        """Test that SQL query caching improves performance."""
        # Clear cache
        _sqlstr_select_archived.cache_clear()

        # Mock the file reading
        with patch("pathlib.Path.open") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                "SELECT archived FROM runs WHERE uuid = ?"
            )

            # First call should read from file
            result1 = _sqlstr_select_archived()

            # Second call should use cache
            result2 = _sqlstr_select_archived()

            # Should return same result
            assert result1 == result2
            # File should only be opened once due to caching
            assert mock_open.call_count == 1

            # Verify cache info
            cache_info = _sqlstr_select_archived.cache_info()
            assert cache_info.hits == 1
            assert cache_info.misses == 1
