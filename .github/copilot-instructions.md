# Copilot Instructions for dttb

## Project Overview

`dttb` (DateTime TraceBack) is a lightweight Python package that attaches timestamps to exception tracebacks. The entire implementation lives in a single module at [src/dttb/__init__.py](../src/dttb/__init__.py).

**Public API** (4 exports only):
- `apply(tz=None, callback=None)` - Hook into `sys.excepthook` and `threading.excepthook`
- `reset()` - Restore original exception hooks
- `Callback` - Type alias for callback functions
- `CallbackArgs` - Named tuple passed to callbacks

## Development Commands

```bash
# Install dependencies
uv sync --dev

# Run linter and formatter
uv run ruff check .
uv run ruff format .

# Run type checker
uv run ty check

# Run tests (unittest, not pytest)
uv run python -m unittest discover tests/

# Run tests with coverage
uv run coverage run -m unittest discover tests/
uv run coverage report
```

## Code Conventions

### Python Version Compatibility
- Support Python 3.8-3.14 (no walrus operator, no `|` union syntax in annotations)
- Use `from __future__ import annotations` for forward references
- Use `Optional[X]` instead of `X | None`
- Use `typing` module imports for type hints

### Module Structure
- All code in `__init__.py` - this is intentional for a small, focused package
- Private functions prefixed with `_` (e.g., `_now`, `_print_dt`, `_log_dttb`)
- Store original hooks in module-level variables (`_sys_excepthook`, `_threading_excepthook`)

### Logging Pattern
- Logger uses `NullHandler()` by default to prevent "No handler found" warnings
- Users configure the `"dttb"` logger externally if they want log output
- Exceptions are logged with `exc_info=exc_value` parameter

### Testing Patterns
- Use `unittest.TestCase`, not pytest
- Capture stderr via `io.StringIO` replacement
- Use `self.assertLogs("dttb", level="ERROR")` for log assertions
- Reset hooks in `setUp()` and `tearDown()` to ensure test isolation
- Use regex pattern `r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d+)?\]"` for timestamp validation

## Tooling

- **Package manager**: [uv](https://github.com/astral-sh/uv) - always use `uv run` for development commands
- **Linter/Formatter**: [ruff](https://github.com/astral-sh/ruff) - configured in pyproject.toml
- **Type checker**: [ty](https://github.com/astral-sh/ty) - use `uv run ty check`
- **Build backend**: `uv_build` (not setuptools or hatchling)

## Documentation

- MkDocs with Material theme and mkdocstrings
- API docs auto-generated from docstrings: [docs/api.md](../docs/api.md)
- Docstrings use Google style with `Attributes:` and `Args:` sections
