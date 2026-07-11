#!/usr/bin/env python3
"""
Automated tests for the skills CI validation pipeline.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALIDATE_SH = SCRIPTS / "validate-skill.sh"


def _bash_executable() -> str:
    """Resolve a usable bash executable across Linux/macOS/Windows."""
    git_bash = Path("C:/Program Files/Git/bin/bash.exe")
    if git_bash.exists():
        return str(git_bash)
    bash = shutil.which("bash")
    if bash and "system32" not in bash.lower():
        return bash
    pytest.skip("bash is required to run validate-skill.sh")


def _to_bash_path(path: Path) -> str:
    """Convert a Windows path to Git Bash /mnt-style path."""
    s = str(path)
    if len(s) > 2 and s[1] == ":":
        drive = s[0].lower()
        rest = s[2:].replace("\\", "/")
        return f"/{drive}{rest}"
    return s.replace("\\", "/")


def run_validate(skill_dir: Path) -> subprocess.CompletedProcess:
    bash = _bash_executable()
    if bash.lower().endswith("bash.exe"):
        cmd = f"bash {_to_bash_path(VALIDATE_SH)} {_to_bash_path(skill_dir)}"
        return subprocess.run(
            [bash, "-lc", cmd],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
    return subprocess.run(
        [bash, str(VALIDATE_SH), str(skill_dir)],
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
    """Regression tests against the real installed skill."""

    def test_cat_architectural_standards_exists_and_validates(self):
        live = Path("/home/workdir/.grok/skills/cat-architectural-standards")
        if not live.exists():
            pytest.skip("Live skill not present in this environment")
        result = run_validate(live)
        assert result.returncode == 0, result.stderr + result.stdout
        assert "cat-architectural-standards" in result.stdout

    def test_cat_skill_has_version(self):
        live = Path("/home/workdir/.grok/skills/cat-architectural-standards/SKILL.md")
        if not live.exists():
            pytest.skip("Live skill not present")
        content = live.read_text(encoding="utf-8")
        assert 'version: "1.0.0"' in content or "version: '1.0.0'" in content or "version: 1.0.0" in content

    def test_cat_skill_has_changelog(self):
        changelog = Path("/home/workdir/.grok/skills/cat-architectural-standards/references/CHANGELOG.md")
        if not changelog.exists():
            pytest.skip("Changelog not present")
        assert changelog.stat().st_size > 0


if __name__ == "__main__":
    # Allow running directly: python tests/test_validate_skill.py
    sys.exit(pytest.main([__file__, "-v"]))