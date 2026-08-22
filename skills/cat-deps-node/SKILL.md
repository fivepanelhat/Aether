---
name: cat-deps-node
description: Use when auditing, pinning, or upgrading Node/npm dependencies in CAT TypeScript hubs (Front_Line_Whanau, CAT-mail, scaffylads). Covers package.json, lockfiles, npm audit, and Dependabot npm. Trigger phrases include npm audit, package.json deps, Node dependencies, Next.js dependencies.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: No analytics SDKs without opt-in labelled path
---

# CAT Deps — Node

## When to use

- package.json changes on TS/Next repos
- npm audit / GHSA on JS ecosystem
- Lockfile conflicts after merges

## Standards

1. **Commit the lockfile**.
2. CI installs with **frozen lockfile** where supported (`npm ci`).
3. Run **npm audit** on non-trivial upgrades; document accepted risks.
4. After dep change: eslint + typecheck + **build** with placeholder env (`build-ci-hygiene`).
5. Prefer dependencies that do not phone-home by default; label any telemetry.

## Upgrade sequence

```text
1. Branch cat/deps-<package>
2. Bump + refresh lockfile
3. npm ci && npm audit
4. lint + tsc + build
5. PR via cat-pr-ship
```

## Related

- `cat-deps`, `cat-code-quality`, `build-ci-hygiene`, `hub-nextjs-component`
