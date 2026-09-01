# Aether skills (Super Grok + CAT)

Skills live under `skills/` and are loaded by `aether.skills.loader.SkillLoader`.

Full catalogue: [SKILLS_CATALOG.md](./SKILLS_CATALOG.md).

**1 September 2026:** skills and the private CAT Agent Harness were created and updated for NZ-Start-Up and related products. This public page does not describe those procedures. Notice: [SKILLS_HARNESS_UPDATE_2026-09-01.md](./SKILLS_HARNESS_UPDATE_2026-09-01.md).

## Super Grok governance skills (2026-07 / hardened 2026-08-24 + practical utilities 2026-08-26)

| Skill | Role | Version |
|-------|------|---------|
| `aether-core` | Primary orchestrator HITL protocol for Aether work | active |
| `aether-skills-ci` | Validate / version / CI skills | active |
| `cat-architectural-standards` | Gold / Platinum / Diamond maturity + HITL gates | active |
| `aether-git-workflow` | Safe git with approval gates | active |
| `aether-skill-authoring` | How to write new skills (hardened + self-improvement against fixed eval set) | **1.2.0** |
| `aether-nz-ai-safety` | NZ AI safety (Algorithm Charter, MBIE, Te Mana Raraunga) | active |
| `aether-hitl-protocol` | Gate levels L0–L4 + **Non-Recursive Core** (immutable fixed points) | **1.1.0** |
| `aether-eval-harness` | Eval layers + Bounded Recursion + **Second-Order / Meta-Eval Lane** | **1.3.0** |
| `aether-skill-composition` | Ordered shortlists + recursive limit + trajectory proposals (L2 only) | **0.3.0** |
| `aether-night-cycle` | Overnight loop + Morning Brief + **Recursive Improvement Proposals** surface | **1.1.0** |

## Super Grok domain skills (2026-07-19)

| Skill | Role | Status |
|-------|------|--------|
| `grants-agent` | Maori AI / agritech / deeptech grants discover-fit-draft-track | active |
| `cat-egress-sentinel` | Offline-native data egress monitor (report-first, HITL) | draft |
| `cat-model-sentinel` | Edge model integrity / drift / silent-swap detection | draft |

**grants-agent source:** Super Grok chat *Maori AI startups - Grants and Funding* (2026-07-19).  
Canonical funding board (when present): `fivepanelhat/.github/funding`.

## NZ Start-Up fleet (embedded)

Under `skills/nz-startup/` (synced from [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up)):

- Public role cards only for the Founder OS working set
- Load via `nz-startup-fleet-bridge` + `agent-hardening`
- Commercial-track procedures stay in the private harness

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

## Hardening notes

- **2026-08-24**: Bounded recursion, immutable evaluation ruler, Non-Recursive Core.
- **2026-08-26**: Practical recursive utilities — meta-eval lane, trajectory proposals only, authoring self-improvement against fixed eval set, Night Cycle as Morning Brief surface for all recursive proposals.
- **2026-09-01**: Skills and private harness updated for NZ-Start-Up and related products. Public Aether does not publish those procedures.

See root [CHANGELOG.md](../CHANGELOG.md) Unreleased section.
