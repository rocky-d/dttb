# Copilot Instructions for dttb

## Project Overview

`dttb` (DateTime TraceBack) is a lightweight Python package that attaches timestamps to exception tracebacks. The entire implementation lives in a single module at [`src/dttb/__init__.py`](../src/dttb/__init__.py).

## Tooling

- Package manager: [uv](https://github.com/astral-sh/uv) - always use `uv run` for development commands
- Linter/Formatter: [ruff](https://github.com/astral-sh/ruff) - configured in pyproject.toml
- Type checker: [ty](https://github.com/astral-sh/ty) - use `uv run ty check`
- Test framework: unittest
- Build backend: uv_build

## Code Conventions

### Python Version Compatibility
- Support Python 3.8-3.14 (no walrus operator, no `|` union syntax in annotations)
- Use `from __future__ import annotations` for forward references
- Use `Optional[X]` instead of `X | None`
- Use `typing` module imports for type hints

### Implementation Details
- All code in `__init__.py` - this is intentional for a small, focused package
- Private functions prefixed with `_` (e.g., `_now`, `_print_dt`, `_log_dttb`)
- Store original hooks in module-level variables (`_sys_excepthook`, `_threading_excepthook`)

## Documentation

- Docstrings use Google style
- MkDocs with Material theme and mkdocstrings

## Agent Skills

- See [`.github/skills/`](./skills/)

## GitHub Actions

- See [`.github/workflows/`](./workflows/)
