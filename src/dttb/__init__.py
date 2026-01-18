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


def _dt() -> None:
    now = dt.datetime.now()
    print(f"[{now}]", file=sys.stderr)


def _log_exc(
    exc_value: Optional[BaseException],
) -> None:
    _logger.error(
        "An uncaught exception logged by dttb:\n",
        exc_info=exc_value,
    )


def _dttb_sys_excepthook(
    func: _SysExcepthook,
) -> _SysExcepthook:
    @functools.wraps(func)
    def wrapper(
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ) -> Any:
        _log_exc(exc_value)
        _dt()
        return func(exc_type, exc_value, exc_traceback)

    return wrapper


def _dttb_threading_excepthook(
    func: _ThreadingExcepthook,
) -> _ThreadingExcepthook:
    @functools.wraps(func)
    def wrapper(
        args: ExceptHookArgs,
    ) -> object:
        _log_exc(args.exc_value)
        _dt()
        return func(args)

    return wrapper


def apply() -> None:
    sys.excepthook = _dttb_sys_excepthook(_sys_excepthook)
    threading.excepthook = _dttb_threading_excepthook(_threading_excepthook)


def reset() -> None:
    sys.excepthook = _sys_excepthook
    threading.excepthook = _threading_excepthook
