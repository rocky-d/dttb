"""
DateTime TraceBack

PyPI: https://pypi.org/project/dttb/
GitHub: https://github.com/rocky-d/dttb
"""

from __future__ import annotations

import datetime as dt
import functools
import logging
import sys
import threading
from threading import ExceptHookArgs
from types import TracebackType
from typing import Any, Callable, Optional, Type

__all__ = [
    "apply",
    "reset",
]


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())

_sys_excepthook = sys.excepthook
_threading_excepthook = threading.excepthook

_SysExcepthook = Callable[
    [Type[BaseException], BaseException, Optional[TracebackType]],
    Any,
]
_ThreadingExcepthook = Callable[
    [ExceptHookArgs],
    object,
]


def _now(
    tz: Optional[dt.tzinfo] = None,
) -> dt.datetime:
    return dt.datetime.now(tz=tz)


def _print_dt(
    now: dt.datetime,
) -> None:
    print(f"[{now}]", file=sys.stderr)


def _log_dttb(
    now: dt.datetime,
    exc_value: Optional[BaseException],
) -> None:
    _logger.error(
        f"An uncaught exception logged by dttb:\n[{now}]\n",
        exc_info=exc_value,
    )


def _dttb_sys_excepthook(
    tz: Optional[dt.tzinfo] = None,
) -> Callable[[_SysExcepthook], _SysExcepthook]:
    def decorator(
        func: _SysExcepthook,
    ) -> _SysExcepthook:
        @functools.wraps(func)
        def wrapper(
            exc_type: Type[BaseException],
            exc_value: BaseException,
            exc_traceback: Optional[TracebackType],
        ) -> Any:
            now = _now(tz=tz)
            _log_dttb(now, exc_value)
            _print_dt(now)
            return func(exc_type, exc_value, exc_traceback)

        return wrapper

    return decorator


def _dttb_threading_excepthook(
    tz: Optional[dt.tzinfo] = None,
) -> Callable[[_ThreadingExcepthook], _ThreadingExcepthook]:
    def decorator(
        func: _ThreadingExcepthook,
    ) -> _ThreadingExcepthook:
        @functools.wraps(func)
        def wrapper(
            args: ExceptHookArgs,
        ) -> object:
            now = _now(tz=tz)
            _log_dttb(now, args.exc_value)
            _print_dt(now)
            return func(args)

        return wrapper

    return decorator


def apply(
    tz: Optional[dt.tzinfo] = None,
) -> None:
    """Applies attaching datetime to exception traceback.

    This also supports logging and threading if involved.

    Args:
        tz: An optional `datetime.tzinfo` object used to determine the timezone of the
            timestamp. If `None` or not given, the local timezone is used.
    """
    sys.excepthook = _dttb_sys_excepthook(tz=tz)(_sys_excepthook)
    threading.excepthook = _dttb_threading_excepthook(tz=tz)(_threading_excepthook)


def reset() -> None:
    """Resets to the default exception traceback."""
    sys.excepthook = _sys_excepthook
    threading.excepthook = _threading_excepthook
