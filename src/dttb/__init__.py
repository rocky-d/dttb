from __future__ import annotations

import datetime as dt
import sys
import threading
import traceback as tb
from types import TracebackType

__all__ = [
    "apply",
]


def _sys_excepthook(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType | None,
) -> None:
    print(f"[{dt.datetime.now()}]", end=" ", file=sys.stderr)
    tb.print_exception(
        exc_type,
        exc_value,
        exc_traceback,
    )


def _threading_excepthook(
    args: threading.ExceptHookArgs,
) -> None:
    print(f"[{dt.datetime.now()}]", end=" ", file=sys.stderr)
    tb.print_exception(
        args.exc_type,
        args.exc_value,
        args.exc_traceback,
    )


def apply() -> None:
    sys.excepthook = _sys_excepthook
    threading.excepthook = _threading_excepthook
