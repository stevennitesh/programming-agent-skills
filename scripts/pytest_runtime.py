"""Keep pytest's disposable state isolated from Windows sandbox identities."""

from __future__ import annotations

import shutil
import stat
import uuid
from pathlib import Path
from typing import Any

import pytest


SESSION_PREFIX = "pytest-session-"
SESSION_ATTRIBUTE = "_programming_agent_skills_pytest_session"


def _retry_writable(function: Any, path: str, error: BaseException) -> None:
    """Retry removal after clearing a Windows read-only bit."""
    del error
    Path(path).chmod(stat.S_IWRITE)
    function(path)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Any) -> None:
    """Give this pytest process fresh temp and cache roots."""
    if config.option.basetemp is not None:
        return

    repository = Path(config.rootpath).resolve()
    session = repository / ".tmp" / f"{SESSION_PREFIX}{uuid.uuid4()}"
    session.mkdir(parents=True)
    setattr(config, SESSION_ATTRIBUTE, session)

    config.option.basetemp = str(session / "tmp")
    config._inicache["cache_dir"] = str(session / "cache")


def remove_session(config: Any) -> None:
    """Remove only the session directory created by this plugin."""
    session = getattr(config, SESSION_ATTRIBUTE, None)
    if session is None:
        return

    session = Path(session).resolve()
    expected_parent = Path(config.rootpath).resolve() / ".tmp"
    if session.parent != expected_parent or not session.name.startswith(SESSION_PREFIX):
        return

    shutil.rmtree(session, onexc=_retry_writable)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    """Remove disposable state after pytest and its cache finish writing."""
    del exitstatus
    remove_session(session.config)
