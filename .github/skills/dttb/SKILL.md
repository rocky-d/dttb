---
name: dttb
description: Guide for using dttb, a Python package that attaches timestamps to exception tracebacks. Use this when debugging Python scripts, working with unknown exception timings, or configuring error logging.
---

# dttb

`dttb` (DateTime TraceBack) is a lightweight Python package that modifies exception handling to verify *when* an error occurred by attaching a timestamp to the traceback output.

## When to use dttb

Use `dttb` when you need to:
- Correlate console errors with log files.
- Debug long-running scripts where the time of failure is important.
- Monitor exception timing in multi-threaded applications.

## Basic Usage

To enable timestamped tracebacks, import `dttb` and call `apply()` at the start of your script:

```python
import dttb

dttb.apply()

# ... rest of your code ...
```

**Output example:**

```text
[2026-02-05 14:30:15.123456]
Traceback (most recent call last):
  ...
Error: something wrong
```

## Advanced Configuration

### Specifying Timezone

You can pass a timezone object to `apply()` to control the timestamp format:

```python
import datetime as dt
import dttb

dttb.apply(tz=dt.timezone.utc)
```

### Custom Callbacks

You can provide a custom callback function to execute additional logic (like sending alerts) when an exception occurs:

```python
import dttb

def my_callback(args: dttb.CallbackArgs) -> None:
    print(f"Exception occurred at {args.now}: {args.exc_value}")

dttb.apply(callback=my_callback)
```

The callback receives a `CallbackArgs` object containing:
- `now`: The timestamp of the exception.
- `exc_type`: The exception class.
- `exc_value`: The exception instance.
- `traceback`: The traceback object.
- `thread`: The thread object (or `None` for main thread).

### Resetting

To restore the original exception hooks (remove timestamps):

```python
dttb.reset()
```

### Integration with Logging

`dttb` can log uncaught exceptions to a specific logger named `"dttb"`. By default, this logger has a `NullHandler`. To capture these logs:

```python
import logging
import dttb

# Configure the dttb logger
logger = logging.getLogger("dttb")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler("errors.log")
logger.addHandler(handler)

dttb.apply()
```

This will ensure uncaught exceptions are written to `errors.log` as well as stderr.
