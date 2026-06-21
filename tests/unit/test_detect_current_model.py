"""Unit tests for lib/detect_current_model.py.

Exercises the REAL public API of the module:
    detect_model_from_env, detect_model_from_process, detect_model_from_marker,
    get_default_model, detect_current_model, create_marker_file, update_session_file

The module is dependency-free at import time (psutil is optional and guarded
inside the function), so the import below is unconditional on purpose: a failed
import is a genuine regression and must fail the suite loudly instead of being
silently skipped.

Tests are isolated from the real environment: model-related env vars are
cleared, the working directory is moved to a temp dir (the marker file is read
from a path relative to cwd), and process detection is driven by a fake psutil
so results are deterministic regardless of the host.
"""

import json
import os
import sys
import types

import pytest

# Make lib/ importable when run standalone (conftest.py also does this).
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))

from detect_current_model import (
    create_marker_file,
    detect_current_model,
    detect_model_from_env,
    detect_model_from_marker,
    detect_model_from_process,
    get_default_model,
    update_session_file,
)

MODEL_ENV_VARS = ["ANTHROPIC_MODEL", "CLAUDE_MODEL", "MODEL_NAME", "AI_MODEL"]


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all model-related env vars so detection is deterministic."""
    for var in MODEL_ENV_VARS:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def isolated_cwd(monkeypatch, tmp_path):
    """Run inside an empty dir so the relative marker file can't leak in."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _fake_psutil(cmdline):
    """Build a stand-in psutil module whose parent process has `cmdline`."""
    fake = types.ModuleType("psutil")

    class _FakeProc:
        def parent(self):
            return self

        def cmdline(self):
            return cmdline

    fake.Process = lambda: _FakeProc()
    return fake


# --- detect_model_from_env --------------------------------------------------


@pytest.mark.parametrize(
    "var,method",
    [
        ("ANTHROPIC_MODEL", "env_anthropic_model"),
        ("CLAUDE_MODEL", "env_claude_model"),
        ("MODEL_NAME", "env_model_name"),
        ("AI_MODEL", "env_ai_model"),
    ],
)
def test_detect_model_from_env_each_var(monkeypatch, clean_env, var, method):
    monkeypatch.setenv(var, "test-model-x")
    assert detect_model_from_env() == ("test-model-x", method)


def test_detect_model_from_env_none_when_unset(clean_env):
    assert detect_model_from_env() == (None, None)


def test_detect_model_from_env_anthropic_takes_precedence(monkeypatch, clean_env):
    monkeypatch.setenv("ANTHROPIC_MODEL", "anthropic-one")
    monkeypatch.setenv("CLAUDE_MODEL", "claude-two")
    assert detect_model_from_env() == ("anthropic-one", "env_anthropic_model")


def test_detect_model_from_env_empty_value_falls_through(monkeypatch, clean_env):
    # An empty string is falsy, so detection must skip it and use the next var.
    monkeypatch.setenv("ANTHROPIC_MODEL", "")
    monkeypatch.setenv("CLAUDE_MODEL", "valid-model")
    assert detect_model_from_env() == ("valid-model", "env_claude_model")


# --- detect_model_from_marker -----------------------------------------------


def test_detect_model_from_marker_reads_content(isolated_cwd):
    marker = isolated_cwd / ".claude-patterns" / "model_marker.txt"
    marker.parent.mkdir(parents=True)
    marker.write_text("My Custom Model")
    assert detect_model_from_marker() == ("My Custom Model", "marker_file")


def test_detect_model_from_marker_none_when_absent(isolated_cwd):
    assert detect_model_from_marker() == (None, None)


def test_detect_model_from_marker_none_when_blank(isolated_cwd):
    marker = isolated_cwd / ".claude-patterns" / "model_marker.txt"
    marker.parent.mkdir(parents=True)
    marker.write_text("   ")
    assert detect_model_from_marker() == (None, None)


# --- get_default_model ------------------------------------------------------


def test_get_default_model_returns_claude_by_default(monkeypatch):
    monkeypatch.setattr("platform.node", lambda: "some-laptop")
    assert get_default_model() == "Claude Sonnet 4.5"


def test_get_default_model_detects_glm_from_node(monkeypatch):
    monkeypatch.setattr("platform.node", lambda: "glm-workstation")
    assert get_default_model() == "GLM 4.6"


# --- detect_model_from_process ----------------------------------------------


def test_detect_model_from_process_parses_claude_sonnet(monkeypatch):
    monkeypatch.setitem(sys.modules, "psutil", _fake_psutil(["claude", "sonnet", "4.5"]))
    assert detect_model_from_process() == ("Claude Sonnet 4.5", "process_cmdline")


def test_detect_model_from_process_parses_glm(monkeypatch):
    monkeypatch.setitem(sys.modules, "psutil", _fake_psutil(["glm", "4.6", "run"]))
    assert detect_model_from_process() == ("GLM 4.6", "process_cmdline")


def test_detect_model_from_process_none_when_no_indicator(monkeypatch):
    monkeypatch.setitem(sys.modules, "psutil", _fake_psutil(["bash", "-c", "echo hi"]))
    assert detect_model_from_process() == (None, None)


def test_detect_model_from_process_handles_missing_psutil(monkeypatch):
    # None in sys.modules forces `import psutil` to raise ImportError, which the
    # function must swallow and report as "not detected".
    monkeypatch.setitem(sys.modules, "psutil", None)
    assert detect_model_from_process() == (None, None)


# --- detect_current_model (integration of the above) ------------------------


def test_detect_current_model_uses_env(monkeypatch, clean_env, isolated_cwd):
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-test-model")
    info = detect_current_model()
    assert info["current_model"] == "claude-test-model"
    assert info["detection_method"] == "env_anthropic_model"
    assert info["confidence"] == "high"
    assert "timestamp" in info


def test_detect_current_model_prefers_marker_over_env(monkeypatch, clean_env, isolated_cwd):
    monkeypatch.setenv("ANTHROPIC_MODEL", "from-env")
    marker = isolated_cwd / ".claude-patterns" / "model_marker.txt"
    marker.parent.mkdir(parents=True)
    marker.write_text("from-marker")
    info = detect_current_model()
    assert info["current_model"] == "from-marker"
    assert info["detection_method"] == "marker_file"


def test_detect_current_model_falls_back_to_default(monkeypatch, clean_env, isolated_cwd):
    # No marker, no env var, and a fake psutil that yields no indicator.
    monkeypatch.setitem(sys.modules, "psutil", _fake_psutil([]))
    info = detect_current_model()
    assert info["detection_method"] == "default_fallback"
    assert info["confidence"] == "low"
    assert info["current_model"]  # non-empty default


# --- create_marker_file / update_session_file -------------------------------


def test_create_marker_file_roundtrip(isolated_cwd):
    create_marker_file("Round Trip Model")
    # detect_model_from_marker reads the relative .claude-patterns path (== cwd).
    assert detect_model_from_marker() == ("Round Trip Model", "marker_file")


def test_update_session_file_writes_expected_fields(monkeypatch, clean_env, isolated_cwd):
    monkeypatch.setenv("CLAUDE_MODEL", "session-model")
    patterns_dir = isolated_cwd / "patterns"
    info = update_session_file(patterns_dir=str(patterns_dir))

    session_file = patterns_dir / "current_session.json"
    assert session_file.exists()

    data = json.loads(session_file.read_text(encoding="utf-8"))
    assert data["current_model"] == "session-model"
    assert data["auto_detected"] is True
    assert data["detection_method"] == info["detection_method"]
    assert "session_start" in data
