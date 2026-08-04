# Alignment Metrics — Scorecard & Hardening Protocol

**Purpose**  
Turn alignment *claims* into measurable, reviewable evidence. Prevents “aligned with Te Mana Raraunga / Algorithm Charter / NZ AI Strategy” from being asserted without controls that can be checked.

**Status**  
Draft — Alignment Week hardening (27 July 2026).  
**Owner**  
Coastal Alpine Tech  

**Related**  
- `docs/alignments/GOVERNANCE-COMPLIANCE-TRUST.md`  
- `docs/alignments/SECURITY-PROTOCOL-ALIGNMENT.md`  
- `skills/te-mana-raraunga-controls` (Minimum Viable Set + checklist)  
- `skills/aether-agent-performance` (CPST / half-life pattern)  
- `docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md`  

---

## 1. Design rules

1. **Evidence over assertion.** Every metric requires an artefact path, log, test, or ADR as proof.
2. **Fail-closed scoring.** Missing evidence = Fail for that control, not “unknown / N/A” that can be waved through for high-stakes claims.
3. **Claim discipline.** External language may only match the *lowest* score tier the system has actually achieved.
4. **Repo-scoped.** Score the system under review (Aether, Front_Line_Whanau, Core, …), not the whole portfolio by default.
5. **Human sign-off.** Any public or grant claim still requires founder (or designated) approval even when metrics pass.

---

## 2. Score tiers

| Tier | Meaning | External language allowed (examples) |
|------|---------|--------------------------------------|
| **L0 — Intent** | Principles documented; no runtime proof | “Designed with regard to…” (internal only) |
| **L1 — Designed** | Controls specified in ADRs / skills; not yet enforced in runtime | “Designed in accordance with…” |
| **L2 — Implemented** | Controls present in code/config; logs or tests exist | “Implements … through [named controls]” |
| **L3 — Measured** | Controls exercised under realistic load; metrics recorded | “Measured alignment against [scorecard date]” |
| **L4 — Assured** | Independent or formal review; residual risk accepted | Reserved; requires external/formal process |

**Default for CAT pre-revenue systems:** target **L2** for production/pilot paths; **L3** for any investor, funder, or public claim.

---

## 3. Core metric families

### A. Sovereignty & Te Mana Raraunga (weight: critical)

| ID | Metric | Pass condition | Evidence |
|----|--------|----------------|----------|
| S1 | Runtime Sovereignty Gate coverage | 100% of off-box / external-model paths pass through fail-closed gate | Gate code path + denial logs |
| S2 | Consent check before personal/cultural access | 0 unguarded access paths in reviewed surface | Consent service calls / tests |
| S3 | Local-first / NZ residency | Default local or NZ; every exception has recorded justification | Config + justification register |
| S4 | Encryption + key control | At-rest + in-transit for high-sensitivity; no unilateral operator decryption for taonga class | Key policy + config |
| S5 | HITL L2+ on sovereignty-affecting changes | 100% of location/key/consent/external-flow changes gated | HITL audit trail |
| S6 | Minimum Viable Set completeness | All 6 MVS items Pass | `te-mana-raraunga-controls` checklist |

**Family pass:** S1–S6 all Pass → sovereignty family = L2 minimum. Any Fail on S1, S2, or S5 → family = Fail for external claims.

### B. Safety & HITL (weight: critical)

| ID | Metric | Pass condition | Evidence |
|----|--------|----------------|----------|
| H1 | Default gate for production / health / cultural / external | L2 or higher | Policy + skill frontmatter / runtime |
| H2 | Agents do not present as final authority | No auto-send / auto-pay / auto-file without human | Code review + tests |
| H3 | SecurityGuard (or equivalent) on model paths | Every agent/portal model path screened | Guard integration tests |
| H4 | High-stakes claim approval | Public success-rate or alignment claims require founder approval | Approval record |

### C. Transparency & Algorithm Charter spirit (weight: high)

| ID | Metric | Pass condition | Evidence |
|----|--------|----------------|----------|
| T1 | Audit trail of prompts / tools / decisions / overrides | Structured logs retained for review window | Log samples |
| T2 | Human-readable audit view exists or is planned with date | Available or scheduled | Docs / ticket |
| T3 | Risk tier assigned for new high-impact features | Tier recorded before production | ADR / risk register |

### D. Performance & economics (weight: medium — required for performance claims)

| ID | Metric | Pass condition | Evidence |
|----|--------|----------------|----------|
| P1 | Cost-per-successful-task defined for the workflow | Formula + sample | Eval artefact |
| P2 | Baseline success rate measured (n ≥ 20) | Recorded under stated conditions | Eval artefact |
| P3 | Half-life estimated or monitoring plan set | Date or threshold | Night Cycle / eval notes |
| P4 | Routing (if used) never bypasses S/H constraints | Policy + sample trajectories | Routing logs |

### E. Claim hygiene (weight: critical for external statements)

| ID | Metric | Pass condition | Evidence |
|----|--------|----------------|----------|
| C1 | Claim maps to named controls | Each external sentence → control IDs | Claim register |
| C2 | No forbidden language without L4 / formal process | Scan of public materials | Review checklist |
| C3 | Third-party benchmarks not presented as CAT results | Clear attribution | Docs / decks |

---

## 4. Composite score (per repo / system)

```
Sovereignty family:  Pass | Fail
Safety/HITL family:  Pass | Fail
Transparency family: Pass | Fail | Partial
Performance family:  Pass | Fail | N/A (if no performance claim)
Claim hygiene:       Pass | Fail
```

**Rules**
- If Sovereignty or Safety/HITL or Claim hygiene = **Fail** → overall = **Fail** for external alignment claims.
- Overall tier = minimum tier among families that apply (see §2).
- Performance family is **N/A** only when no ROI / success-rate / CPST claim is made.

---

## 5. Measurement cadence

| Cadence | Action |
|---------|--------|
| Per feature / PR (high-stakes) | S1–S5, H1–H3 smoke against the change |
| Before pilot / production | Full MVS checklist + scorecard signed |
| Before grant / investor / public claim | Full scorecard + C1–C3 + founder approval |
| Quarterly (or post-incident) | Re-run scorecard; update half-life / CPST if claimed |

---

## 6. Repo scorecard template (copy per system)

See `docs/alignments/scorecards/TEMPLATE.md`.

Store completed scorecards under `docs/alignments/scorecards/` (or project eval artefacts) with a clear date.

---

## 7. Hardening actions (immediate)

1. Run the MVS checklist (`skills/te-mana-raraunga-controls/references/checklist.md`) on Front_Line_Whanau and Aether production paths.
2. Create first scorecards for **Aether** and **Front_Line_Whanau** (highest claim risk).
3. Add claim register rows for any live grant or website language.
4. Do not promote experimental skills’ claims to “measured” until P1–P2 exist for a real workflow.
5. Optional: apply `proposed-inserts.md` only after first scorecards are signed.

---

## 8. Anti-patterns

- Scoring “Pass” because documentation exists without runtime proof.
- Using portfolio-level narrative to cover a single weak repo.
- Publishing CPST or success rates without n, method, and environment.
- Treating L1 Designed as sufficient for public “aligned with Te Mana Raraunga” claims.
- Letting cost or speed metrics override S1–S5 or H1–H3.

---

Coastal Alpine Tech · Aether  
Alignment Metrics v0.1.0 · 27 July 2026
