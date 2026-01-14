# dttb

[![pypi](https://img.shields.io/pypi/v/dttb.svg)](https://pypi.org/project/dttb/)
[![python](https://img.shields.io/pypi/pyversions/dttb.svg)](https://pypi.org/project/dttb/)
[![license](https://img.shields.io/pypi/l/dttb.svg)](https://github.com/rocky-d/dttb/blob/main/LICENSE)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

**D**ate**T**ime **T**race**B**ack

## Usage

```python
import dttb

dttb.apply()

1 / 0
```

```plaintext
[2026-01-08 18:11:50.767093] Traceback (most recent call last):
  File "/Users/rockydu/Projects/dttb/demo.py", line 5, in <module>
    1 / 0
ZeroDivisionError: division by zero
```
