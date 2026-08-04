# MVS Runtime Gap Plan — Path to L2

**Date:** 2026-07-27  
**Owner:** Coastal Alpine Tech  
**Authorised with:** Alignment scorecards founder sign-off (L1 / L0–L1)  
**Goal:** Move **Aether** and especially **Front_Line_Whanau** from Designed (L1) to Implemented (L2) on the Alignment Metrics scorecard.

**Rule:** No public Te Mana Raraunga / Charter “aligned” claim for Hub until this plan’s Must items have evidence links on a re-scored card.

---

## Minimum Viable Set (reminder)

| Order | Control | Priority |
|-------|---------|----------|
| 1 | **X2** Runtime Sovereignty Gate (fail-closed) | Must |
| 2 | **X1** Consent check before personal/cultural access | Must |
| 3 | **R2 + Kt2** Local-first / NZ residency preference | Must |
| 4 | **Kt1 + R3** Encryption + owner-influenced keys | Must |
| 5 | **X4** HITL L2+ on sovereignty-affecting changes | Must (policy exists) |
| 6 | **W1 + X3** Provenance + sovereignty metadata | Must |

---

## Phase A — Spec & interfaces (Aether, this week)

| Task | Repo | Deliverable | Done when |
|------|------|-------------|-----------|
| A1 | Aether | TypeScript interfaces: `SovereigntyGateRequest` / `Decision`, `ConsentCheck` | Types in `types/` or Core package; exported |
| A2 | Aether | Fail-closed gate pseudocode + unit tests (deny on missing consent / unknown residency) | Tests red→green for deny paths |
| A3 | Aether | Wire gate call site checklist for every external-model / off-box path | Checklist ADR + code comments or middleware list |
| A4 | Aether | HITL L2 binding verified on gate override and key/consent/location changes | Policy test or skill frontmatter audit |

**Out of scope for Phase A:** Full production consent graph UI.

---

## Phase B — Hub hardening (Front_Line_Whanau, highest priority)

| Task | Deliverable | Done when |
|------|-------------|-----------|
| B1 | Consent + purpose-binding on personal/cultural data access | No unguarded read/write in reviewed routes; tests |
| B2 | Runtime Sovereignty Gate on all external model calls | Denial logs exist; fail-closed without approval |
| B3 | Default HITL L2+ for health-adjacent and cultural outputs | Config/policy enforced in agent paths |
| B4 | Medical / funding disclaimers on relevant generations | Content gate or template always applied |
| B5 | Cultural review pathway documented | Runbook + owner named |
| B6 | Agents never present clinical advice as authority | Prompt + eval cases |

**Pilot LOI language:** Blocked until B1–B4 Pass on a new scorecard.

---

## Phase C — Evidence & re-score

| Task | Deliverable |
|------|-------------|
| C1 | Attach evidence links (PRs, logs, tests) to scorecard rows |
| C2 | Re-run Alignment Scorecard for Aether and Front_Line_Whanau |
| C3 | Update CLAIM-REGISTER if any external sentence is proposed |
| C4 | Only then consider L2 language in grants |

---

## Interface sketch (Phase A1)

```typescript
/** Fail-closed pre-flight before off-box or external-model transfer */
export interface SovereigntyGateRequest {
  purpose: string;
  sensitivity: "public" | "internal" | "restricted" | "taonga";
  dataClasses: string[];
  destination: "local" | "nz-resident" | "external";
  consentRef?: string;
  hitlApprovalRef?: string;
  actor: "agent" | "user" | "system";
}

export type SovereigntyGateDecision =
  | { allow: true; conditions?: string[] }
  | { allow: false; reason: string; required: ("consent" | "hitl" | "residency" | "encryption")[] };
```

Default: if any required check cannot be completed → `{ allow: false }`.

---

## Non-goals

- Claiming L2 without tests/logs  
- Bypassing gate for “cost” or “latency”  
- Public grant language ahead of Phase C  

---

## Related

- `docs/alignments/ALIGNMENT-METRICS.md`  
- `docs/alignments/scorecards/2026-07-27-*.md`  
- `skills/te-mana-raraunga-controls`  
- `docs/alignments/SECURITY-PROTOCOL-ALIGNMENT.md`  

Coastal Alpine Tech · Aether  
MVS Runtime Gap Plan v0.1.0 · 27 July 2026
