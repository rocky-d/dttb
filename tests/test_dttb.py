import io
import logging
import sys
import threading
import unittest
from unittest.mock import MagicMock, patch

import dttb


class TestDTTB(unittest.TestCase):
    # Regex pattern for timestamp format [YYYY-MM-DD HH:MM:SS.xxxxxx]
    TIMESTAMP_PATTERN = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?\]"

    def setUp(
        self,
    ) -> None:
        # Ensure environment is reset before each test
        dttb.reset()

        # Capture stderr
        self.stderr_capture = io.StringIO()
        self.orig_stderr = sys.stderr
        sys.stderr = self.stderr_capture

        # Save original hook references for comparison
        self.orig_sys_hook = dttb._sys_excepthook
        self.orig_threading_hook = dttb._threading_excepthook

    def tearDown(
        self,
    ) -> None:
        dttb.reset()
        sys.stderr = self.orig_stderr
        self.stderr_capture.close()

    def test_apply_changes_hooks(
        self,
    ) -> None:
        """Test if apply modifies sys and threading excepthook."""
        dttb.apply()
        self.assertNotEqual(sys.excepthook, self.orig_sys_hook)
        self.assertNotEqual(threading.excepthook, self.orig_threading_hook)

    def test_reset_restores_hooks(
        self,
    ) -> None:
        """Test if reset restores original hooks."""
        dttb.apply()
        dttb.reset()
        self.assertEqual(sys.excepthook, self.orig_sys_hook)
        self.assertEqual(threading.excepthook, self.orig_threading_hook)

    def test_sys_excepthook_output(
        self,
    ) -> None:
        """Test if sys.excepthook triggers timestamp output."""
        dttb.apply()

        # Invoke current excepthook with simulated exception info
        sys.excepthook(ValueError, ValueError("test error"), None)

        output = self.stderr_capture.getvalue()
        self.assertRegex(output, self.TIMESTAMP_PATTERN)
        self.assertIn("ValueError", output)

    def test_threading_excepthook_output(
        self,
    ) -> None:
        """Test if threading.excepthook triggers timestamp output."""
        dttb.apply()

        # Construct ExceptHookArgs
        args = threading.ExceptHookArgs(
            [ValueError, ValueError("thread error"), None, threading.current_thread()]
        )

        threading.excepthook(args)

        output = self.stderr_capture.getvalue()
        self.assertRegex(output, self.TIMESTAMP_PATTERN)
        self.assertIn("ValueError", output)

    def test_apply_idempotency_structural(
        self,
    ) -> None:
        """Test structural behavior of multiple apply calls."""
        dttb.apply()
        hook1 = sys.excepthook

        dttb.apply()
        hook2 = sys.excepthook

        # Each apply generates a new wrapper instance
        self.assertNotEqual(hook1, hook2)

        # Verify functionality remains normal after multiple applies
        sys.excepthook(ValueError, ValueError("test"), None)
        self.assertRegex(self.stderr_capture.getvalue(), self.TIMESTAMP_PATTERN)

    def test_alternating_apply_reset(
        self,
    ) -> None:
        """Test alternating usage of apply and reset."""
        dttb.apply()
        # Confirm hook changed
        self.assertNotEqual(sys.excepthook, self.orig_sys_hook)

        dttb.reset()
        # Confirm hook restored
        self.assertEqual(sys.excepthook, self.orig_sys_hook)

        dttb.apply()
        # Confirm hook changed again
        self.assertNotEqual(sys.excepthook, self.orig_sys_hook)

    def test_real_thread_exception(
        self,
    ) -> None:
        """Test exception raised in a real separate thread."""
        dttb.apply()

        def failing_task() -> None:
            raise ValueError("native thread error")

        t = threading.Thread(target=failing_task)
        t.start()
        t.join()

        output = self.stderr_capture.getvalue()
        # Verify timestamp is printed
        self.assertRegex(output, self.TIMESTAMP_PATTERN)
        # Verify exception message is caught and printed
        self.assertIn("native thread error", output)

    def test_logging_output(
        self,
    ) -> None:
        """Test if exceptions are logged to the dttb logger."""
        dttb.apply()

        # Use assertLogs to verify logging output
        with self.assertLogs("dttb", level="ERROR") as cm:
            sys.excepthook(ValueError, ValueError("logging test"), None)

        self.assertTrue(len(cm.output) > 0)
        self.assertIn("An uncaught exception logged by dttb", cm.output[0])

        # Test threading logging
        with self.assertLogs("dttb", level="ERROR") as cm:
            args = threading.ExceptHookArgs(
                [ValueError, ValueError("thread logging test"), None, None]
            )
            threading.excepthook(args)

        self.assertTrue(len(cm.output) > 0)
        self.assertIn("An uncaught exception logged by dttb", cm.output[0])

    def test_logger_has_null_handler_by_default(
        self,
    ) -> None:
        """Verify that the logger has a NullHandler by default to prevent 'No handler found' warnings."""
        logger = logging.getLogger("dttb")
        # Check if any of the handlers is a NullHandler
        has_null_handler = any(
            isinstance(h, logging.NullHandler) for h in logger.handlers
        )
        self.assertTrue(has_null_handler, "dttb logger should have a NullHandler")

    @patch("dttb._logger")
    def test_logging_with_exc_info(
        self,
        mock_logger: MagicMock,
    ) -> None:
        """Verify that logger.error is called with exc_info=True/Exception."""
        dttb.apply()

        exc = ValueError("test exc info")
        sys.excepthook(ValueError, exc, None)

        # Verify logger.error was called
        mock_logger.error.assert_called_once()

        # Check arguments
        args, kwargs = mock_logger.error.call_args
        self.assertIn("An uncaught exception logged by dttb", args[0])
        self.assertEqual(kwargs.get("exc_info"), exc)

    def test_logging_real_thread_exception(
        self,
    ) -> None:
        """Test if exceptions in real threads are logged to the dttb logger."""
        dttb.apply()

        def failing_task() -> None:
            raise ValueError("real thread logging error")

        with self.assertLogs("dttb", level="ERROR") as cm:
            t = threading.Thread(target=failing_task)
            t.start()
            t.join()

        self.assertTrue(len(cm.output) > 0)
        self.assertIn("real thread logging error", cm.output[0])
