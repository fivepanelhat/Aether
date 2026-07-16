# Aether skills (Super Grok + CAT)

Skills live under `skills/` and are loaded by `aether.skills.loader.SkillLoader`.

## Super Grok governance skills (2026-07)

| Skill | Role |
|-------|------|
| `aether-core` | Primary orchestrator HITL protocol for Aether work |
| `aether-skills-ci` | Validate / version / CI skills |
| `cat-architectural-standards` | Gold / Platinum / Diamond maturity + HITL gates |
| `aether-git-workflow` | Safe git with approval gates |
| `aether-skill-authoring` | How to write new skills |

## NZ Start-Up fleet (embedded)

Under `skills/nz-startup/` (synced from [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up)):

- formation, compliance, grants/RDTI, market, GTM, finance, legal, board CoS
- **`first-principles-operator`** - digital employee P0 brief (`nz-startup operate`)
- Load via `nz-startup-fleet-bridge` + `agent-hardening`

## CI

```bash
# Structural validation (Git Bash / Linux)
bash scripts/validate-skill.sh skills/aether-core

# Version checks
python scripts/check-skill-versions.py

# Skills CI unit tests
pip install -r requirements-test.txt
python -m pytest tests/skills_ci/ -v
```

Workflow: `.github/workflows/skills-ci.yml` runs on `skills/**` changes.

## Autonomy

Agents **inform, draft, prepare, monitor, remind**.  
Humans **advise, sign, file, send, pay**.

Cultural / health / production changes always require explicit HITL approval.
