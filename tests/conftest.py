"""Pytest configuration for the repository test suite."""

from typing import Any

import pytest

from scripts import pytest_runtime


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Any) -> None:
    pytest_runtime.pytest_configure(config)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    pytest_runtime.pytest_sessionfinish(session, exitstatus)
