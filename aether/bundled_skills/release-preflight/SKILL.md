---
name: release-preflight
description: Mandatory pre-release checks that prevent tag collisions, version/tag mismatches, sensitive files leaking into public repos, and out-of-order fix application. Run before any commit/tag/push/release sequence.
version: "1.0.0"
type: security
requires_hitl: true
cultural_sensitivity: medium
tags:
  - release
  - git
  - security
  - preflight
  - publish
---

# Release Preflight

## Overview
Automated agents executing release sequences (`git add -A; commit; tag; push`) fail in
predictable ways: they recreate existing tags, tag versions that don't match the version
file, sweep untracked sensitive documents into public repositories, and apply fix
bundles out of order. This skill makes those failures impossible to reach by requiring
`scripts/release_preflight.py` to pass before ANY release command runs.

Real incidents this skill encodes (Aether, July 2026):
1. A v0.5.0 tag was pushed pointing at a commit NEWER than v0.6.0 (fix zips applied in
   reverse order), inverting release history.
2. `git tag v0.6.1` failed because the tag already existed; the agent deleted and
   recreated it — recoverable, but only because a human reviewed the output.
3. `INVESTOR_ONE_PAGER.md` sat untracked in a PUBLIC repo, one `git add -A` away from
   publishing confidential valuation figures to every scraper watching GitHub.

## When to Use
- Before every `git tag`, `git push --tags`, or `gh release create`
- Before any bulk `git add -A` in a repository with public visibility
- As the first step of any agent-executed release workflow
- In CI, as a required job gating the release pipeline

## Instructions
1. Run the preflight script from the repo root and STOP on any failure:
   ```bash
   python scripts/release_preflight.py --version <intended-version>
   ```
2. The script enforces, in order:
   - **Visibility awareness**: detects whether the remote is public; if public, scans
     untracked and staged files against the sensitive-name blocklist (investor, valuation,
     financial, credential, secret, .env, one-pager, board-pack, term-sheet).
   - **Tag collision**: the intended tag must not already exist locally or on the remote.
   - **Monotonic versions**: the intended version must be greater than every existing
     semver tag — prevents inverted release history.
   - **Version-file agreement**: `aether/__init__.py` `__version__` must equal the
     intended version (single source of truth; pyproject reads it dynamically).
   - **Clean tree**: no unstaged modifications; untracked files must be explicitly
     acknowledged with `--allow-untracked <path>` (no silent `add -A` sweeps).
   - **Tests green**: full pytest suite passes.
3. Only after exit code 0 may the release sequence proceed.
4. HITL: a human confirms the printed summary (visibility, files to be published,
   tag, version) before push. Never bypass this confirmation.

## Guardrails & Constraints
- NEVER use `git add -A` in a public repo without a preflight pass in the same session.
- NEVER delete-and-recreate a remote tag without explicit human approval — moving
  published tags breaks downstream consumers.
- Sensitive-pattern matches are a hard stop, not a warning, when the repo is public.
- Te Mana Raraunga alignment: data about people and communities (funding documents,
  community-partner details, marae deployment specifics) must never reach a public
  remote without explicit kaitiaki approval.
