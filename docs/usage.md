# Usage

## Applying

**`demo1.py`**

```python
import dttb

dttb.apply()

1 / 0
```

```text
[2026-01-15 22:37:09.882049]
Traceback (most recent call last):
  File "demo1.py", line 5, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

## Resetting

**`demo2.py`**

```python
import dttb

dttb.apply()
dttb.reset()

1 / 0
```

```text
Traceback (most recent call last):
  File "demo2.py", line 4, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

## With *logging*

**`demo3.py`**

```python
import dttb
import logging

dttb_logger = logging.getLogger("dttb")
dttb_logger.propagate = False
dttb_logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler("logging.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
dttb_logger.addHandler(file_handler)

dttb.apply()

1 / 0
```

```text
[2026-01-19 23:29:35.817684]
Traceback (most recent call last):
  File "demo3.py", line 13, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

**`logging.log`**

```log
2026-01-19 23:29:35,817 | ERROR | An uncaught exception logged by dttb:
[2026-01-19 23:29:35.817684]
Traceback (most recent call last):
  File "demo3.py", line 13, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

## With *threading*

**`demo4.py`**

```python
import dttb
import threading
import time

dttb.apply()


def func(seconds):
    time.sleep(seconds)
    seconds / 0


thread1 = threading.Thread(target=func, kwargs={"seconds": 1})
thread2 = threading.Thread(target=func, kwargs={"seconds": 2})
thread1.start()
thread2.start()
thread1.join()
thread2.join()

func(seconds=3)
```

```text
[2026-01-15 23:00:03.048290]
Exception in thread Thread-1:
Traceback (most recent call last):
  ...
  File "demo4.py", line 10, in func
    seconds / 0
ZeroDivisionError: division by zero
[2026-01-15 23:00:04.048362]
Exception in thread Thread-2:
Traceback (most recent call last):
  ...
  File "demo4.py", line 10, in func
    seconds / 0
ZeroDivisionError: division by zero
[2026-01-15 23:00:07.055083]
Traceback (most recent call last):
  File "demo4.py", line 20, in <module>
    func(seconds=3)
  File "demo4.py", line 10, in func
    seconds / 0
ZeroDivisionError: division by zero
```

## Specifying Timezone

**`demo5.py`**

```python
import datetime as dt
import dttb

dttb.apply(tz=dt.timezone.utc)

1 / 0
```

```text
[2026-01-21 02:40:53.353001+00:00]
Traceback (most recent call last):
  File "demo5.py", line 6, in <module>
    1 / 0
ZeroDivisionError: division by zero
```

## Setting Callback

**`demo6.py`**

```python
import dttb


def callback(args: dttb.CallbackArgs) -> None:
    print(f"[callback] {args.now = }")
    print(f"[callback] {args.exc_type = }")
    print(f"[callback] {args.exc_value = }")
    print(f"[callback] {args.thread = } (None indicates the 'MainThread')")


dttb.apply(callback=callback)

1 / 0
```

```text
[2026-01-29 10:31:29.469555]
Traceback (most recent call last):
  File "demo6.py", line 13, in <module>
    1 / 0
ZeroDivisionError: division by zero
[callback] args.now = datetime.datetime(2026, 1, 29, 10, 31, 29, 469555)
[callback] args.exc_type = <class 'ZeroDivisionError'>
[callback] args.exc_value = ZeroDivisionError('division by zero')
[callback] args.thread = None (None indicates the 'MainThread')
```
