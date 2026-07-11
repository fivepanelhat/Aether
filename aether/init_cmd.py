"""
``aether init`` — install bundled skills for the user / project.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .paths import (
    copy_skills_tree,
    project_skills_dir,
    source_skills_dir,
    user_skills_dir,
)


def run_init(
    project: bool = True,
    user: bool = True,
    force: bool = False,
    cwd: Optional[str] = None,
) -> int:
    """
    Copy packaged (or repo) skills into:
    - ~/.aether/skills  (user, always when user=True)
    - ./skills          (project-local when project=True)

    Returns process exit code (0 success, 1 no source skills).
    """
    src = source_skills_dir()
    if src is None:
        print(
            "Error: no bundled skills found. "
            "Reinstall Aether or clone the repo with a skills/ directory."
        )
        return 1

    print("Aether init")
    print(f"  Source skills: {src}")
    any_work = False

    if user:
        stats = copy_skills_tree(src, user_skills_dir(), force=force)
        any_work = True
        print(
            f"  User skills → {stats['dest']} "
            f"(copied={stats['copied']}, skipped_existing={stats['skipped']})"
        )

    if project:
        dest = project_skills_dir(cwd)
        stats = copy_skills_tree(src, dest, force=force)
        any_work = True
        print(
            f"  Project skills → {stats['dest']} "
            f"(copied={stats['copied']}, skipped_existing={stats['skipped']})"
        )

    if not any_work:
        print("  Nothing to do (pass --user and/or --project).")
        return 0

    marker = Path.home() / ".aether"
    marker.mkdir(parents=True, exist_ok=True)
    (marker / "initialized").write_text("ok\n", encoding="utf-8")

    print("\nNext steps:")
    print('  aether skills')
    print('  aether run "Audit the project for security issues"')
    if not force:
        print("  (use --force to overwrite existing skill folders)")
    return 0


def build_init_parser(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser(
        "init",
        help="Install bundled skills to ~/.aether/skills and/or ./skills",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing skill directories",
    )
    p.add_argument(
        "--user-only",
        action="store_true",
        help="Only install to ~/.aether/skills (skip project ./skills)",
    )
    p.add_argument(
        "--project-only",
        action="store_true",
        help="Only install to ./skills (skip ~/.aether/skills)",
    )
