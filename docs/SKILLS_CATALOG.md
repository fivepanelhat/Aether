# Aether Skills Catalog

All skills under `skills/*/SKILL.md` are auto-discovered by the dynamic Skill Loader.  
**Stack companion context (2026-07):** Aether supports the Kiwi Edge AI architecture (RPi 5 16GB + Hailo-10H, Coastal-Alpine-Core, Weaver, portals, firmware) with HITL-first safety.

Run `python -m aether.cli skills` (or `aether skills` when installed) to list loaded skills and descriptions.

---

## Governance & Hardened Skills (2026-08-24 + practical utilities 2026-08-26)

### aether-eval-harness
**Type**: Evaluation · **Priority**: Very High · **Version**: 1.3.0 · **HITL**: yes  
**Description**: Multi-layer eval + Bounded Recursion & Harness Safety + explicit **Second-Order / Meta-Eval Lane** (versioned, proposal-only, fixed evaluation set, L2+ gated).  
**Use when**: Designing success criteria, regression suites, LLM-as-judge lanes, proving agent reliability, meta-evaluation of the harness itself, or any recursive improvement proposal.

### aether-hitl-protocol
**Type**: Governance · **Priority**: Very High · **Version**: 1.1.0 · **HITL**: yes  
**Description**: Gate levels L0–L4, standing policies, approval artefacts. Includes **Non-Recursive Core**: HITL gates, Te Mana Raraunga Must controls, autonomy ceilings and cultural requirements are immutable fixed points. Attempts to rewrite them escalate to L3/L4.  
**Use when**: Designing or reviewing any approval flow, Night Cycle behaviour, or sovereignty-affecting change.

### aether-skill-composition
**Type**: Orchestration · **Priority**: High · **Version**: 0.3.0 · **HITL**: yes  
**Description**: Produces ordered shortlists (2–5 skills). Recursive composition limited to one additional level (outer L2). High-confidence trajectories may *propose* (never auto-apply) updates to composition heuristics or meta-skills.  
**Use when**: Non-trivial multi-skill tasks, planning skill sequences, or any recursive skill chaining.

### aether-skill-authoring
**Type**: Meta · **Priority**: High · **Version**: 1.2.0 · **HITL**: yes  
**Description**: How to create/update skills. Hardened rules + self-improvement against a fixed evaluation set (all changes as diffs + evidence; no auto-merge). L3 escalation for any attempt to touch HITL gates, recursion ceilings or Te Mana Raraunga Must controls.  
**Use when**: Authoring or refining any new or existing skill, including recursive self-improvement of the authoring skill.

### aether-night-cycle
**Type**: Orchestration · **Priority**: High · **Version**: 1.1.0 · **HITL**: yes  
**Description**: Evening summary + prioritised next-day plan + Morning Brief. New **Recursive Improvement Proposals** section: overnight meta/recursive proposals are queued for Morning Brief with source, diff, evidence and required gate; agents may generate but never apply.  
**Use when**: Continuous overnight operation, scheduled agents, morning review of recursive proposals.

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
| Recursive skill / harness work | `aether-skill-composition` → `aether-eval-harness` → `aether-hitl-protocol` → `aether-skill-authoring` |

---

## Format

See [AETHER_SKILL_FORMAT.md](./AETHER_SKILL_FORMAT.md) and [SKILL_DEVELOPMENT_GUIDE.md](./SKILL_DEVELOPMENT_GUIDE.md).  
Meta skill: `skill-creator`.
