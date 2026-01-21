# dttb

[![license](https://img.shields.io/github/license/rocky-d/dttb?logo=github&logoColor=white)](https://github.com/rocky-d/dttb/blob/main/LICENSE)
[![lint](https://img.shields.io/github/actions/workflow/status/rocky-d/dttb/lint.yml?logo=githubactions&logoColor=white&label=lint)](https://github.com/rocky-d/dttb/actions/workflows/lint.yml)
[![test](https://img.shields.io/github/actions/workflow/status/rocky-d/dttb/test.yml?logo=githubactions&logoColor=white&label=test)](https://github.com/rocky-d/dttb/actions/workflows/test.yml)
[![codecov](https://img.shields.io/codecov/c/github/rocky-d/dttb?logo=codecov&logoColor=white)](https://codecov.io/gh/rocky-d/dttb)
[![pypi-v](https://img.shields.io/pypi/v/dttb?logo=pypi&logoColor=white)](https://pypi.org/project/dttb/)
[![pypi-dm](https://img.shields.io/pypi/dm/dttb?logo=pypi&logoColor=white)](https://pypi.org/project/dttb/)
[![sponsors](https://img.shields.io/github/sponsors/rocky-d?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/rocky-d)

[![python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Frocky-d%2Fdttb%2Fmain%2Fpyproject.toml&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

**D**ate**T**ime **T**race**B**ack

## Installation

- **uv**

```sh
uv add dttb
```

- **pip**

```sh
pip install dttb
```

## Usage

### Applying

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

### Resetting

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

### With *logging*

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

### With *threading*

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
  File "/**/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/**/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "demo4.py", line 10, in func
    seconds / 0
ZeroDivisionError: division by zero
[2026-01-15 23:00:04.048362]
Exception in thread Thread-2:
Traceback (most recent call last):
  File "/**/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/**/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
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

### Specifying Timezone

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
