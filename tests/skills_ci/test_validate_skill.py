#!/usr/bin/env python3
"""
Automated tests for the skills CI validation pipeline.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# tests/skills_ci/ -> repo root is parents[2]
ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALIDATE_PY = SCRIPTS / "validate_skill.py"
VALIDATE_SH = SCRIPTS / "validate-skill.sh"


def run_validate(skill_dir: Path) -> subprocess.CompletedProcess:
    # Prefer cross-platform Python validator (bash often unavailable on Windows)
    if VALIDATE_PY.is_file():
        return subprocess.run(
            [sys.executable, str(VALIDATE_PY), str(skill_dir)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    return subprocess.run(
        ["bash", str(VALIDATE_SH), str(skill_dir)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


class TestValidateSkillScript:
    def test_good_skill_passes(self):
        result = run_validate(FIXTURES / "good-skill")
        assert result.returncode == 0, result.stderr + result.stdout
        assert "OK: Skill 'good-skill' is valid" in result.stdout

    def test_bad_name_fails(self):
        result = run_validate(FIXTURES / "bad-name")
        assert result.returncode != 0
        assert "must match" in result.stderr.lower() or "must match" in result.stdout.lower()

    def test_missing_description_fails(self):
        result = run_validate(FIXTURES / "missing-description")
        assert result.returncode != 0
        assert "description" in result.stderr.lower() or "description" in result.stdout.lower()

    def test_versioned_skill_passes(self):
        result = run_validate(FIXTURES / "versioned-skill")
        assert result.returncode == 0, result.stderr + result.stdout
        assert "metadata.version present" in result.stdout or "OK:" in result.stdout

    def test_nonexistent_dir_fails(self):
        result = run_validate(FIXTURES / "does-not-exist")
        assert result.returncode != 0


class TestVersionChecker:
    def test_version_checker_runs(self):
        """The version checker should at least execute without crashing."""
        checker = SCRIPTS / "check-skill-versions.py"
        # Run against the fixtures directory by temporarily treating it as root
        # (we just verify the script is importable / runnable)
        result = subprocess.run(
            [sys.executable, str(checker)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        # It may return 0 or 1 depending on whether it finds skills, but it must not crash
        assert result.returncode in (0, 1), result.stderr


class TestLiveCatArchitecturalStandards:
    """Regression tests against the repo skill (Super Grok pack)."""

    def test_cat_architectural_standards_exists_and_validates(self):
        live = ROOT / "skills" / "cat-architectural-standards"
        if not live.exists():
            pytest.skip("Live skill not present in this environment")
        result = run_validate(live)
        assert result.returncode == 0, result.stderr + result.stdout
        assert "cat-architectural-standards" in result.stdout

    def test_cat_skill_has_version(self):
        live = ROOT / "skills" / "cat-architectural-standards" / "SKILL.md"
        if not live.exists():
            pytest.skip("Live skill not present")
        content = live.read_text(encoding="utf-8")
        assert "version:" in content

    def test_cat_skill_has_changelog(self):
        changelog = (
            ROOT / "skills" / "cat-architectural-standards" / "references" / "CHANGELOG.md"
        )
        if not changelog.exists():
            pytest.skip("Changelog not present")
        assert changelog.stat().st_size > 0


if __name__ == "__main__":
    # Allow running directly: python tests/test_validate_skill.py
    sys.exit(pytest.main([__file__, "-v"]))