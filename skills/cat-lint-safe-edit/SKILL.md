---
name: cat-lint-safe-edit
description: Use before bulk formatting, encoding, ASCII-safe, or whitespace sweeps across one or many CAT repos. Prevents collapsed indentation and invalid workflow YAML. Pair with repo-recovery-sweep if damage already occurred. Trigger phrases include lint sweep, format sweep, bulk reformat, encoding sweep, ASCII-safe edit.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: none
  resource_envelope: light
  sovereignty_notes: Validate before push; never push unvalidated multi-file sweeps
---

# CAT Lint-Safe Edit

Prevention skill for bulk edits that historically broke the estate.

## When to use

- About to run repo-wide format, encoding, or whitespace cleanup
- Introducing a new formatter across multiple packages
- Any automated rewrite that touches `.github/workflows/`

## Hard rules

1. **Never** strip or normalise leading whitespace with naive global replace.
2. **Never** push a multi-file sweep without local validation.
3. Validate **before** push:
   - Python: `python -m compileall` on touched packages (or targeted modules)
   - Workflows: YAML parse for each changed workflow
   - Prefer project scripts: `ruff check`, `pytest` subset if available
4. Prefer **scoped** sweeps (one repo, one concern) over org-wide single commits.
5. If Actions shows duration `—` and “Invalid workflow file”, stop and load `repo-recovery-sweep`.

## Safe sequence

```text
1. Branch cat/<topic>
2. Apply tool on limited path
3. Validate (compile + workflow parse + lint)
4. Commit
5. PR with extended description (cat-pr-ship)
6. Merge only after green CI
```

## Related

- `repo-recovery-sweep` — after damage
- `ci-failure-triage` — classify red
- `cat-code-quality` — steady-state gates
- `build-ci-hygiene` — CI shape

## HITL

Org-wide or multi-repo sweeps require L2 founder approval before push to any default branch.
