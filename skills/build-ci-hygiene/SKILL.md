---
name: build-ci-hygiene
description: Prevents module-level env crashes and ensures reliable CI builds with a production build step, least-privilege GitHub Actions permissions, and Dependabot coverage.
version: "0.2.0"
type: hygiene
requires_hitl: false
cultural_sensitivity: low
tags: [ci, github-actions, dependabot, permissions, build]
---

# Build & CI Hygiene

## Overview
Fixes recurring build and CI issues caused by eager module-level code (env parsing, client construction).

## When to Use
- Build fails in clean CI environments but works locally
- Module-level code reads env vars or constructs clients at import time
- CI only runs type-check/lint but not `npm run build`

## Instructions
1. Make env parsing lazy (use Proxy or deferred validation).
2. Make external clients (Supabase, Tavily, LLM, etc.) lazy-loaded inside handlers.
3. Add a `next build` (or equivalent) step to CI with placeholder env vars.
4. Verify clean builds on fresh checkouts.
5. **Actions token scope** - every workflow must declare `permissions:` (default `contents: read`; release jobs may use minimal write scopes). Fixes CodeQL `actions/missing-workflow-permissions`.
6. **Dependabot** - ensure `.github/dependabot.yml` covers the repo ecosystems (`pip` / `npm` / `github-actions` as applicable).
7. Prefer Node 24 / Python versions already standardised on the Kiwi Edge estate.

## Guardrails & Constraints
- Never construct clients or parse secrets at module load time.
- CI must run a full production build, not just type/lint checks.
- Do not use broad default `GITHUB_TOKEN` write access on PR CI.
- Cross-check with `security-notifications-triage` for open alerts.
