from unittest.mock import MagicMock, patch

from nnlogging.funcs import add_branch, remove_branch
from nnlogging.options import ConsoleFullOpt, FilterFullOpt, HandlerFullOpt
from nnlogging.typings import Branches


class TestBranchFuncs:
    @patch("nnlogging.funcs._branch.get_rconsole")
    @patch("nnlogging.funcs._branch.get_rhandler")
    @patch("nnlogging.funcs._branch.get_logfilter")
    @patch("nnlogging.funcs._branch.attach_handler_logfilter")
    @patch("logging.getLogger")
    def test_add_branch(
        self,
        mock_get_logger,
        mock_attach,
        mock_get_logfilter,
        mock_get_rhandler,
        mock_get_rconsole,
    ):
        # Setup mocks
        mock_console = MagicMock()
        mock_handler = MagicMock()
        mock_filter = MagicMock()
        mock_logger = MagicMock()

        mock_get_rconsole.return_value = mock_console
        mock_get_rhandler.return_value = mock_handler
        mock_get_logfilter.return_value = mock_filter
        mock_get_logger.return_value = mock_logger

        branches: Branches = {}
        sinks = [("sink1", "stdout")]
        logger = "test_logger"
        console_kwargs = ConsoleFullOpt()
        handler_kwargs = HandlerFullOpt()
        filter_kwargs = FilterFullOpt()

        add_branch(
            branches,
            sinks,
            logger=logger,
            console_kwargs=console_kwargs,
            handler_kwargs=handler_kwargs,
            filter_kwargs=filter_kwargs,
        )

        # Verify mocks
        mock_get_rconsole.assert_called_once_with("stdout", console_kwargs)
        mock_get_rhandler.assert_called_once_with(mock_console, handler_kwargs)
        mock_get_logfilter.assert_called_once_with(None)
        mock_attach.assert_called_once_with(mock_handler, mock_filter)
        mock_logger.addHandler.assert_called_once_with(mock_handler)

        # Verify branches update
        assert "sink1" in branches
        branch = branches["sink1"]
        assert branch["logger"] == logger
        assert branch["console"] == mock_console
        assert branch["handler"] == mock_handler
        assert branch["filter"] == mock_filter
        assert branch["tasks"] == {}

    @patch("nnlogging.funcs._branch.detach_handler_logfilter")
    @patch("logging.getLogger")
    def test_remove_branch_without_progress(self, mock_get_logger, mock_detach):
        # Setup mocks
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_handler = MagicMock()
        mock_filter = MagicMock()
        branches: Branches = {
            "sink1": {
                "logger": "test_logger",
                "console": MagicMock(),
                "handler": mock_handler,
                "filter": mock_filter,
                "tasks": {},
            }
        }

        remove_branch(branches, ["sink1"])

        # Verify mocks
        mock_handler.close.assert_called_once()
        mock_logger.removeHandler.assert_called_once_with(mock_handler)
        mock_detach.assert_called_once_with(mock_handler, mock_filter)

        # Verify removal
        assert "sink1" not in branches

    @patch("nnlogging.funcs._branch.detach_handler_logfilter")
    @patch("logging.getLogger")
    def test_remove_branch_with_progress(self, mock_get_logger, mock_detach):
        # Setup mocks
        mock_logger = MagicMock()
        mock_progress = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_handler = MagicMock()
        mock_filter = MagicMock()
        branches: Branches = {
            "sink1": {
                "logger": "test_logger",
                "console": MagicMock(),
                "handler": mock_handler,
                "filter": mock_filter,
                "tasks": {},
                "progress": mock_progress,
            }
        }

        remove_branch(branches, ["sink1"])

        # Verify mocks
        mock_handler.close.assert_called_once()
        mock_logger.removeHandler.assert_called_once_with(mock_handler)
        mock_detach.assert_called_once_with(mock_handler, mock_filter)
        mock_progress.stop.assert_called_once()

        # Verify removal
        assert "sink1" not in branches
