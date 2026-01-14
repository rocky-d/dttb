import io
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

    @patch("dttb._dt")
    def test_dt_called(
        self,
        mock_dt: MagicMock,
    ) -> None:
        """Use mock to verify _dt is called correctly."""
        dttb.apply()

        # Test sys hook
        sys.excepthook(ValueError, ValueError("test"), None)
        self.assertEqual(mock_dt.call_count, 1)

        # Test threading hook
        args = threading.ExceptHookArgs([ValueError, ValueError("t"), None, None])
        threading.excepthook(args)
        self.assertEqual(mock_dt.call_count, 2)

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
