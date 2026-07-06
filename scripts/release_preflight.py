#!/usr/bin/env python3
"""
Aether Release Preflight — stdlib only.

Run from the repo root before any tag/push/release:
    python scripts/release_preflight.py --version 0.6.2

Exit code 0 = safe to release. Any other exit code = STOP.

Checks (in order):
  1. Remote visibility (public repos get strict sensitive-file scanning)
  2. Sensitive filenames among untracked/staged files
  3. Tag collision (local + remote)
  4. Monotonic version (intended > all existing semver tags)
  5. Version file agreement (aether/__init__.py __version__)
  6. Clean working tree (untracked files must be explicitly allowed)
  7. Test suite passes
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

SENSITIVE_PATTERNS = [
    r"investor", r"valuation", r"financial", r"one[-_]?pager", r"board[-_]?pack",
    r"term[-_]?sheet", r"credential", r"secret", r"\.env$", r"\.pem$", r"\.key$",
    r"api[-_]?key", r"password", r"funding[-_]?deck",
]

PASS = "  [PASS]"
FAIL = "  [FAIL]"
WARN = "  [WARN]"


def sh(cmd: list) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout.strip()


def parse_semver(tag: str):
    m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag.strip())
    return tuple(int(x) for x in m.groups()) if m else None


def check_visibility(remote_url: str) -> bool:
    """Returns True if the repo is public (or unknown — treated as public for safety)."""
    m = re.search(r"github\.com[:/]([^/]+)/([^/.]+)", remote_url)
    if not m:
        print(f"{WARN} Could not parse GitHub remote; treating repo as PUBLIC for safety.")
        return True
    owner, repo = m.groups()
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers={"Accept": "application/vnd.github+json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            private = bool(data.get("private", False))
            print(f"{PASS} Remote visibility: {'PRIVATE' if private else 'PUBLIC'} ({owner}/{repo})")
            return not private
    except Exception as e:
        # 404 on an unauthenticated request usually means private; anything else, assume public
        if "404" in str(e):
            print(f"{PASS} Remote not visible unauthenticated — treating as PRIVATE.")
            return False
        print(f"{WARN} Visibility check failed ({e}); treating repo as PUBLIC for safety.")
        return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Aether release preflight")
    parser.add_argument("--version", required=True, help="Intended release version, e.g. 0.6.2")
    parser.add_argument("--allow-untracked", action="append", default=[],
                        help="Explicitly acknowledge an untracked path (repeatable)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip the pytest run (not recommended)")
    args = parser.parse_args()

    intended = args.version.lstrip("v")
    intended_semver = parse_semver(intended)
    failures = 0

    print(f"\n=== AETHER RELEASE PREFLIGHT — v{intended} ===\n")

    if not intended_semver:
        print(f"{FAIL} '{args.version}' is not valid semver (X.Y.Z).")
        return 1

    # --- 1. Visibility ---
    remote_url = sh(["git", "remote", "get-url", "origin"])
    is_public = check_visibility(remote_url)

    # --- 2. Sensitive files ---
    untracked = [l for l in sh(["git", "ls-files", "--others", "--exclude-standard"]).splitlines() if l]
    staged = [l for l in sh(["git", "diff", "--cached", "--name-only"]).splitlines() if l]
    candidates = set(untracked) | set(staged)
    sensitive_hits = sorted(
        f for f in candidates
        if any(re.search(p, f, re.IGNORECASE) for p in SENSITIVE_PATTERNS)
    )
    if sensitive_hits and is_public:
        print(f"{FAIL} Sensitive-looking files present in a PUBLIC repo:")
        for f in sensitive_hits:
            print(f"         - {f}")
        print("         Move to a private location or add to .gitignore before releasing.")
        failures += 1
    elif sensitive_hits:
        print(f"{WARN} Sensitive-looking files present (repo is private): {sensitive_hits}")
    else:
        print(f"{PASS} No sensitive filenames among untracked/staged files.")

    # --- 3. Tag collision ---
    sh(["git", "fetch", "--tags", "--quiet"])
    existing_tags = [t for t in sh(["git", "tag", "-l"]).splitlines() if t]
    for candidate_tag in (f"v{intended}", intended):
        if candidate_tag in existing_tags:
            print(f"{FAIL} Tag '{candidate_tag}' already exists. Choose the next version; never move published tags.")
            failures += 1
            break
    else:
        print(f"{PASS} Tag v{intended} does not exist locally or on the fetched remote.")

    # --- 4. Monotonic version ---
    semver_tags = [(t, parse_semver(t)) for t in existing_tags]
    higher = [t for t, sv in semver_tags if sv and sv >= intended_semver]
    if higher:
        print(f"{FAIL} Existing tag(s) {higher} are >= v{intended}. Releases must be monotonic.")
        failures += 1
    else:
        print(f"{PASS} v{intended} is greater than all {len([s for _, s in semver_tags if s])} existing semver tags.")

    # --- 5. Version file agreement ---
    init_path = Path("aether/__init__.py")
    if init_path.exists():
        m = re.search(r'__version__\s*=\s*"([^"]+)"', init_path.read_text(encoding="utf-8"))
        file_version = m.group(1) if m else None
        if file_version == intended:
            print(f"{PASS} aether/__init__.py __version__ == {intended}.")
        else:
            print(f"{FAIL} aether/__init__.py says '{file_version}' but releasing v{intended}. Fix the file first.")
            failures += 1
    else:
        print(f"{FAIL} aether/__init__.py not found — run from the repo root.")
        failures += 1

    # --- 6. Clean tree ---
    # Check for UNSTAGED changes only; staged changes are fine (about to be committed)
    status_lines = sh(["git", "status", "--porcelain"]).splitlines()
    unstaged = [l for l in status_lines if l and len(l) > 1 and l[1] != ' ' and not l.startswith("??")]
    unacknowledged = [f for f in untracked if f not in args.allow_untracked]
    if unstaged:
        print(f"{FAIL} Unstaged modifications present:")
        for l in unstaged[:10]:
            print(f"         {l}")
        failures += 1
    elif unacknowledged:
        print(f"{FAIL} Untracked files not acknowledged (pass --allow-untracked for each intended file):")
        for f in unacknowledged[:10]:
            print(f"         - {f}")
        failures += 1
    else:
        print(f"{PASS} Working tree clean; all untracked files acknowledged.")

    # --- 7. Tests ---
    if args.skip_tests:
        print(f"{WARN} Tests skipped by flag.")
    else:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"],
                                capture_output=True, text=True)
        tail = (result.stdout or result.stderr).strip().splitlines()[-1:] or ["no output"]
        if result.returncode == 0:
            print(f"{PASS} Test suite green: {tail[0]}")
        else:
            print(f"{FAIL} Test suite failed: {tail[0]}")
            failures += 1

    print(f"\n=== RESULT: {'SAFE TO RELEASE' if failures == 0 else f'{failures} BLOCKING ISSUE(S) — DO NOT RELEASE'} ===\n")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
