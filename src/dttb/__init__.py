"""
DateTime TraceBack

- [Homepage](https://pypi.org/project/dttb/)
- [Repository](https://github.com/rocky-d/dttb)
- [Documentation](https://rocky-d.github.io/dttb/)
"""

from __future__ import annotations

import datetime as dt
import functools
import logging
import sys
import threading
from threading import ExceptHookArgs
from types import TracebackType
from typing import Any, Callable, NamedTuple, Optional, Type

__all__ = [
    "Callback",
    "CallbackArgs",
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


class CallbackArgs(NamedTuple):
    now: dt.datetime
    exc_type: Type[BaseException]
    exc_value: Optional[BaseException]
    exc_traceback: Optional[TracebackType]
    thread: Optional[threading.Thread]


Callback = Callable[[CallbackArgs], Any]


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
        f"An uncaught exception logged by dttb:\n[{now}]",
        exc_info=exc_value,
    )


def _dttb_sys_excepthook(
    *,
    tz: Optional[dt.tzinfo] = None,
    callback: Optional[Callback] = None,
) -> Callable[[_SysExcepthook], _SysExcepthook]:
    def decorator(
        excepthook: _SysExcepthook,
    ) -> _SysExcepthook:
        @functools.wraps(excepthook)
        def wrapper(
            exc_type: Type[BaseException],
            exc_value: BaseException,
            exc_traceback: Optional[TracebackType],
        ) -> Any:
            now = _now(tz=tz)
            _log_dttb(now, exc_value)
            _print_dt(now)
            result = excepthook(exc_type, exc_value, exc_traceback)
            if callback is not None:
                callback(
                    CallbackArgs(
                        now,
                        exc_type,
                        exc_value,
                        exc_traceback,
                        None,
                    ),
                )
            return result

        return wrapper

    return decorator


def _dttb_threading_excepthook(
    *,
    tz: Optional[dt.tzinfo] = None,
    callback: Optional[Callback] = None,
) -> Callable[[_ThreadingExcepthook], _ThreadingExcepthook]:
    def decorator(
        excepthook: _ThreadingExcepthook,
    ) -> _ThreadingExcepthook:
        @functools.wraps(excepthook)
        def wrapper(
            args: ExceptHookArgs,
        ) -> object:
            now = _now(tz=tz)
            _log_dttb(now, args.exc_value)
            _print_dt(now)
            result = excepthook(args)
            if callback is not None:
                callback(
                    CallbackArgs(
                        now,
                        args.exc_type,
                        args.exc_value,
                        args.exc_traceback,
                        args.thread,
                    ),
                )
            return result

        return wrapper

    return decorator


def apply(
    *,
    tz: Optional[dt.tzinfo] = None,
    callback: Optional[Callback] = None,
) -> None:
    """Applies attaching datetime to exception traceback.

    This also supports logging and threading if involved.

    Args:
        tz: An optional `datetime.tzinfo` object used to determine the timezone of the
            timestamp. If `None` or not given, the local timezone is used.
        callback: An optional `Callback` object that is called with a `CallbackArgs`
            object as its only argument whenever an uncaught exception occurs.
    """
    sys.excepthook = _dttb_sys_excepthook(
        tz=tz,
        callback=callback,
    )(_sys_excepthook)
    threading.excepthook = _dttb_threading_excepthook(
        tz=tz,
        callback=callback,
    )(_threading_excepthook)


def reset() -> None:
    """Resets to the default exception traceback."""
    sys.excepthook = _sys_excepthook
    threading.excepthook = _threading_excepthook
