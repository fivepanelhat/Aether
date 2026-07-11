#!/usr/bin/env python3
"""
Check skill versioning conventions for Coastal Alpine Tech / Aether skills.

Rules (v1):
- If metadata.version exists it must be valid semver (X.Y.Z)
- Versioned skills should have a CHANGELOG.md (references/ or root)
- All skills in a monorepo should not have duplicate names
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def extract_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return None


def find_skill_dirs(root: Path) -> list[Path]:
    candidates = []
    # Common layouts
    for base in [root / "skills", root]:
        if not base.exists():
            continue
        for p in base.iterdir():
            if p.is_dir() and (p / "SKILL.md").exists():
                candidates.append(p)
    return sorted(set(candidates), key=lambda p: p.name)


def main() -> int:
    root = Path(".").resolve()
    skill_dirs = find_skill_dirs(root)

    if not skill_dirs:
        print("No skill directories found — skipping version checks")
        return 0

    errors = []
    warnings = []
    seen_names: set[str] = set()

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)

        name = skill_dir.name
        if name in seen_names:
            errors.append(f"Duplicate skill name: {name}")
        seen_names.add(name)

        if not fm:
            warnings.append(f"{name}: could not parse frontmatter")
            continue

        meta = fm.get("metadata") or {}
        version = meta.get("version") if isinstance(meta, dict) else None

        if version is None:
            # Not required for all skills yet, but recommended for CAT skills
            if name.startswith(("cat-", "aether-")):
                warnings.append(f"{name}: CAT/Aether skill missing metadata.version")
            continue

        if not isinstance(version, str) or not SEMVER_RE.match(version):
            errors.append(f"{name}: metadata.version '{version}' is not valid semver (X.Y.Z)")

        # Changelog check
        changelog_paths = [
            skill_dir / "references" / "CHANGELOG.md",
            skill_dir / "CHANGELOG.md",
        ]
        if not any(p.exists() for p in changelog_paths):
            warnings.append(f"{name}: versioned skill has no CHANGELOG.md")

    print(f"Checked {len(skill_dirs)} skill(s)")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"FAIL: {e}")

    if errors:
        return 1
    print("Version checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())