#!/usr/bin/env python3
"""Cross-platform skill validator (Windows + Linux). Mirrors validate-skill.sh rules."""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def die(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"OK: {msg}")


def main() -> int:
    if len(sys.argv) != 2:
        die("Usage: validate_skill.py <skill-directory>")
    skill_dir = Path(sys.argv[1])
    expected = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_dir.is_dir():
        die(f"Directory does not exist: {skill_dir}")
    if not skill_md.is_file():
        die(f"SKILL.md not found in {skill_dir}")

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        die("SKILL.md must start with --- (YAML frontmatter)")
    parts = content.split("---", 2)
    if len(parts) < 3:
        die("Empty or malformed frontmatter")
    fm_raw, body = parts[1], parts[2]
    if not body.strip():
        die("SKILL.md body is empty")

    data: dict[str, str] = {}
    for line in fm_raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip().strip('"').strip("'")

    name = data.get("name", "")
    if not name:
        die("Missing 'name' in frontmatter")
    if name != expected:
        die(f"name '{name}' must match directory '{expected}'")
    if not NAME_RE.match(name):
        die(f"name format invalid: {name}")

    desc = data.get("description", "")
    if not desc or desc == ">":
        # folded description may be empty in simple parse - check raw
        if "description:" not in fm_raw:
            die("Missing description")
        ok("description present (folded or scalar)")
    else:
        ok("description present")

    ok(f"Skill '{name}' is valid")
    if "version:" in fm_raw or "metadata:" in fm_raw:
        ok("metadata.version present or metadata block found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
