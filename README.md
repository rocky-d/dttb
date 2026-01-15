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

## Usage

```python
import dttb

dttb.apply()

1 / 0
```

```plaintext
[2026-01-08 18:11:50.767093]
Traceback (most recent call last):
  File "/Users/rockydu/Projects/dttb/demo.py", line 5, in <module>
    1 / 0
ZeroDivisionError: division by zero
```
