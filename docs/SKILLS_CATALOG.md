# Aether Skills Catalog

All skills under `skills/*/SKILL.md` are auto-discovered by the dynamic Skill Loader.  
**Stack companion context (2026-07):** Aether supports the Kiwi Edge AI architecture (RPi 5 16GB + Hailo-10H, Coastal-Alpine-Core, Weaver, portals, firmware) with HITL-first safety.

Run `python -m aether.cli skills` (or `aether skills` when installed) to list loaded skills and descriptions.

---

## Architecture & sovereignty (new)

### kiwi-edge-architecture
**Type**: Orchestration · **Priority**: Very High · **Version**: 1.0.0  
**Description**: Full Kiwi Edge system map — field → fabric → Core SDK → Weaver → portals → Ollama/Hailo → trust plane.  
**Use when**: Working on coastal-alpine-stack, Core, Weaver, portals, firmware, or architecture docs/blurbs.

### security-notifications-triage
**Type**: Security · **Priority**: Very High · **Version**: 1.0.0 · **HITL**: yes  
**Description**: Triage Dependabot/GHSA/CodeQL/pip-audit findings; apply estate patch patterns (workflow permissions, dep floors, SECURITY.md).  
**Use when**: Security notifications, org-wide hardening sprints, advisory response.

### te-mana-raraunga-sovereignty
**Type**: Security · **Priority**: Very High · **Version**: 1.0.0 · **HITL**: yes · **Cultural sensitivity**: high  
**Description**: Enforce Te Mana Raraunga 2018 data-sovereignty constraints (local custody, no silent cloud exfil).  
**Use when**: Data flows, multi-tenant RAG, compliance/portfolio docs, whenua-linked domains.

### aether-nz-ai-safety
**Type**: Safety / Governance · **Priority**: Very High · **Version**: 1.0.0 · **HITL**: yes · **Cultural sensitivity**: high  
**Description**: Hardened NZ AI safety guidelines (Public Service AI Framework, Algorithm Charter, MBIE Responsible AI Guidance + Te Mana Raraunga + fail-closed controls). Risk-tiered HITL mapping and mandatory technical controls.  
**Use when**: Hardening safety policy, reviewing agents/portals for compliance, preparing pilots/grants/investor claims of responsible AI, risk tiering, or Te Tiriti + AI discussions.

### grants-agent
**Type**: Orchestration · **Priority**: Very High · **Version**: 0.1.0 · **HITL**: yes · **Cultural sensitivity**: high  
**Description**: Discover, fit-score, draft, and track funding for CAT projects (Maori AI, agritech, deeptech, sovereign edge). Modes A-E. Never submits without HITL.  
**Use when**: Grants, RDTI, Te Puni Kokiri, MPI PSGF, New to R&D, NZIAT, whenua funds, Kotahitanga capital.  
**Source**: Super Grok (2026-07-19) Maori AI startups - Grants and Funding.

### cat-egress-sentinel
**Type**: Sentinel · **Priority**: High · **Version**: 0.2.0 · **HITL**: yes · **Status**: draft  
**Description**: Context-aware data-egress monitor enforcing offline-native sovereignty (report-first; blocking needs human approval).  
**Use when**: Auditing cloud SDK leakage, offline guarantees, Te Mana Raraunga egress risks.

### cat-model-sentinel
**Type**: Sentinel · **Priority**: High · **Version**: 0.1.0 · **HITL**: no (escalates cultural canary) · **Status**: draft  
**Description**: Edge model availability, latency, integrity, silent-swap and behavioural drift monitor.  
**Use when**: Ollama/YOLO pin checks, model drift, integrity baselines on edge nodes.

---

## Security

| Skill | Priority | Description |
| ----- | -------- | ----------- |
| `security-auth-guard` | Very High | Auth + RBAC on sensitive API routes |
| `security-route-audit` | Very High | Structured API route security audit |
| `error-message-sanitization` | Very High | Block raw error/stack leaks to clients |
| `service-role-key-protection` | Very High | Force `createAdminClient()` patterns |
| `strict-zod-schema-enforcement` | High | Replace `z.any()` with strict Zod |
| `release-preflight` | Very High | Block bad tags, secret sweeps, version skew (HITL) |

---

## Error remediation & CI

| Skill | Priority | Description |
| ----- | -------- | ----------- |
| `error-remediation-orchestrator` | Very High | End-to-end analyze → fix → git (HITL) |
| `ci-failure-parser` | High | Structure CI / Actions logs for remediation |
| `notification-responder` | High | Status updates and approval asks |
| `git-workflow` | High | Branch / commit / push / PR with HITL |
| `build-ci-hygiene` | High | Lazy env, full production builds, least-privilege CI |

---

## Product & platform

| Skill | Priority | Description |
| ----- | -------- | ----------- |
| `agent-reliability-context` | Very High | Multi-turn history, tools, guardrail tuning |
| `hub-nextjs-component` | High | Whānau hub UI — a11y, Te Tiriti-aware |
| `design-system-unification` | High | Tokens, theme, visual consistency |
| `schema-migration-hygiene` | High | Safe DB migrations + indexes (HITL) |
| `project-scaffolder` | High | Scaffold new projects with stack norms |
| `release-engineering` | High | Version, build, test, tag, release |
| `skill-creator` | Medium | Author and iterate new skills |

---

## Suggested stacks

| Goal | Skill sequence |
| ---- | -------------- |
| Harden a portal API | `security-route-audit` → `security-auth-guard` → `strict-zod-schema-enforcement` → `error-message-sanitization` |
| Fix CI on main | `ci-failure-parser` → `error-remediation-orchestrator` → `git-workflow` |
| Touch Core / stack architecture | `kiwi-edge-architecture` → `te-mana-raraunga-sovereignty` → `security-notifications-triage` |
| Org security sprint | `security-notifications-triage` → `build-ci-hygiene` → `release-preflight` |
| Whānau hub UI | `hub-nextjs-component` → `design-system-unification` → `te-mana-raraunga-sovereignty` |
| AI safety / compliance claims | `aether-nz-ai-safety` → `aether-hitl-protocol` → `te-mana-raraunga-sovereignty` |

---

## Format

See [AETHER_SKILL_FORMAT.md](./AETHER_SKILL_FORMAT.md) and [SKILL_DEVELOPMENT_GUIDE.md](./SKILL_DEVELOPMENT_GUIDE.md).  
Meta skill: `skill-creator`.
