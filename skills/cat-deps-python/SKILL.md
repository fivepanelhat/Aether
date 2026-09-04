---
name: cat-deps-python
description: Use when auditing, pinning, or upgrading Python dependencies in CAT edge repos (Core, Weaver, stack, portals, harness). Covers pyproject.toml, requirements*.txt, uv/pip, pip-audit, and Dependabot pip. Trigger phrases include pip-audit, pyproject deps, Python dependencies, requirements upgrade.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: Prefer deps that work offline; document any telemetry SDK
---

# CAT Deps — Python

## When to use

- Adding or upgrading a Python package on the edge stack
- pip-audit / safety findings
- Aligning pyproject vs requirements files

## Standards

1. Prefer **pyproject.toml** as source of truth when the repo already has it.
2. Production/runtime deps stay **minimal** for edge/RPi targets.
3. Dev deps in optional extras (`[dev]`, `[test]`).
4. Run **pip-audit** (or estate SecOps equivalent) before merging non-trivial upgrades.
5. After dep change: ruff + pytest on touched area (`cat-code-quality`).
6. Do not add cloud-only SDKs to core edge paths without explicit profile flag.

## Upgrade sequence

```text
1. Branch cat/deps-<package>-<version>
2. Bump pin
3. Install from lock/requirements
4. pip-audit
5. lint + tests
6. PR via cat-pr-ship
```

## Related

- `cat-deps`, `cat-code-quality`, `build-ci-hygiene`, `secops-ci-estate-scan`
