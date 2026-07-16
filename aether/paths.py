"""
Path helpers for Aether - skills discovery and package data.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import List, Optional


def package_root() -> Path:
 """Directory containing the ``aether`` package (site-packages/aether or src)."""
 return Path(__file__).resolve().parent


def repo_skills_dir() -> Optional[Path]:
 """
 Skills at the repository root (editable installs / git checkout).
 package is <repo>/aether -> parent is <repo>.
 """
 candidate = package_root().parent / "skills"
 if candidate.is_dir() and any(candidate.iterdir()):
 return candidate
 return None


def bundled_skills_dir() -> Optional[Path]:
 """Skills shipped inside the wheel under ``aether/bundled_skills``."""
 candidate = package_root() / "bundled_skills"
 if candidate.is_dir() and any(candidate.iterdir()):
 return candidate
 return None


def user_skills_dir() -> Path:
 return Path.home() / ".aether" / "skills"


def project_skills_dir(cwd: Optional[str] = None) -> Path:
 return Path(cwd or os.getcwd()) / "skills"


def resolve_skills_directory(explicit: Optional[str] = None) -> Optional[str]:
 """
 Resolve the skills directory in priority order:
 1. Explicit argument (used even if empty - for tests / core mode)
 2. AETHER_SKILLS_DIR environment variable
 3. ./skills relative to the current working directory
 4. ~/.aether/skills
 5. Packaged aether/bundled_skills (wheel / sdist install)
 6. Repo-root skills/ (editable checkout next to the package)
 Returns the first existing directory that should be used, or None.
 Auto-discovered dirs must be non-empty; explicit/env may be empty.
 """
 if explicit:
 p = Path(explicit)
 if p.is_dir():
 return str(p.resolve())
 return None

 env_dir = os.environ.get("AETHER_SKILLS_DIR")
 if env_dir:
 p = Path(env_dir)
 if p.is_dir():
 return str(p.resolve())

 candidates: List[Optional[Path]] = [
 project_skills_dir(),
 user_skills_dir(),
 bundled_skills_dir(),
 repo_skills_dir(),
 ]

 for candidate in candidates:
 if candidate is None:
 continue
 try:
 if candidate.is_dir() and any(candidate.iterdir()):
 return str(candidate.resolve())
 except OSError:
 continue
 return None


def source_skills_dir() -> Optional[Path]:
 """Best source tree for ``aether init`` to copy from (prefer bundled, then repo)."""
 return bundled_skills_dir() or repo_skills_dir()


def copy_skills_tree(src: Path, dest: Path, force: bool = False) -> dict:
 """
 Copy skill folders from src -> dest.
 Returns stats: {copied, skipped, source, dest}.
 """
 dest.mkdir(parents=True, exist_ok=True)
 copied, skipped = 0, 0
 for child in sorted(src.iterdir()):
 if not child.is_dir():
 continue
 target = dest / child.name
 if target.exists() and not force:
 skipped += 1
 continue
 if target.exists() and force:
 shutil.rmtree(target)
 shutil.copytree(child, target)
 copied += 1
 return {
 "copied": copied,
 "skipped": skipped,
 "source": str(src),
 "dest": str(dest),
 }


def _norm_for_compare(p: str) -> str:
 """Normalize path for equality/containment checks (case-fold on Windows)."""
 p = os.path.realpath(os.path.abspath(p))
 # Strip trailing separators so "C:\\proj\\" and "C:\\proj" compare equal
 p = os.path.normpath(p)
 if os.name == "nt":
 p = os.path.normcase(p)
 return p


def is_within_allowed_root(path: str, allowed_root: str) -> bool:
 """
 True if ``path`` resolves inside ``allowed_root`` (no traversal).

 Portable across Linux and Windows:
 - Uses ``os.path.commonpath`` (handles drive letters / different roots)
 - Case-insensitive comparison on Windows (``normcase``)
 - Works with mixed ``/`` and ``\\`` separators
 """
 try:
 root = _norm_for_compare(allowed_root)
 resolved = _norm_for_compare(path)
 except (OSError, ValueError):
 return False

 try:
 common = os.path.commonpath([root, resolved])
 except ValueError:
 # Different drives on Windows (e.g. C:\\ vs D:\\)
 return False

 if os.name == "nt":
 common = os.path.normcase(os.path.normpath(common))
 else:
 common = os.path.normpath(common)

 return common == root


def ensure_utf8_stdio() -> None:
 """Best-effort UTF-8 stdout/stderr on Windows consoles (no-op if unsupported)."""
 import sys

 for stream_name in ("stdout", "stderr"):
 stream = getattr(sys, stream_name, None)
 if stream is None:
 continue
 reconfigure = getattr(stream, "reconfigure", None)
 if callable(reconfigure):
 try:
 reconfigure(encoding="utf-8", errors="replace")
 except Exception:
 pass
