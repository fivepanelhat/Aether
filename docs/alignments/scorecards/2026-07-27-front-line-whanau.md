# Alignment Scorecard — Front_Line_Whanau

**Date:** 2026-07-27  
**Reviewer:** Alignment Week draft (founding review pending)  
**Scope:** Whānau Preterm Support Hub (Front_Line_Whanau) — health-adjacent, cultural, and personal data paths  
**Protocol:** `docs/alignments/ALIGNMENT-METRICS.md` v0.1.0  
**Repo map:** `docs/alignments/repo-maps/front-line-whanau.md`  

---

## Families

| Family | Result | Tier | Evidence links / notes |
|--------|--------|------|------------------------|
| Sovereignty (S1–S6) | **Fail for external claims** | L0–L1 | Highest sensitivity domain. Principles and Hub architecture align on paper; Runtime Sovereignty Gate, consent graph, and MVS **not** evidenced as production-enforced in this pass. |
| Safety / HITL (H1–H4) | **Partial** | L1 | Design intent: default L2+ for personal/health/cultural content. Must be verified in Hub agent paths and UI before pilot claims. No auto-actuate assumed. |
| Transparency (T1–T3) | **Partial** | L1 | Charter spirit requires human-readable audit of significant decisions. Confirm logging for resource recommendations and any agent-mediated advice. |
| Performance (P1–P4) | **N/A** | — | No performance/ROI claim in scope for this scorecard. |
| Claim hygiene (C1–C3) | **Pass (if claims withheld)** | — | Safe posture: make **no** public “Te Mana Raraunga aligned” or Charter-aligned claim until S/H families Pass at L2. |

---

## Minimum Viable Set

| Control | Pass / Fail | Evidence |
|---------|-------------|---------|----------|
| X2 Runtime Sovereignty Gate | **Fail** | Not evidenced on Hub external-model / off-box paths |
| X1 Consent check | **Fail / unverified** | Explicit consent + purpose-binding called out as gap in repo map |
| R2 + Kt2 Local-first / NZ residency | **Unverified** | Architecture intent local-first; residency exceptions not scored this pass |
| Kt1 + R3 Encryption + key control | **Unverified** | Required for health-adjacent data; not evidenced here |
| X4 HITL L2+ on sovereignty changes | **Pass (policy intent)** | Repo map: Critical HITL; must be wired in production flows |
| W1 + X3 Provenance + metadata | **Unverified** | Required for whānau / cultural records |

---

## Domain-specific requirements (Hub)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Cultural review pathway documented and ready | Gap | Repo map next action |
| Medical / funding disclaimers on relevant outputs | Gap | Must gate generation |
| No external model for restricted/taonga without recorded approval | Gap | Depends on X2 + HITL |
| Agents do not give clinical advice as authority | Policy | Keep non-negotiable |

---

## Overall

**Tier:** **L0–L1 (Intent / Designed)**  
**External language allowed:**  
- Internal design notes only until MVS evidence exists  
- **Not allowed** for pilot marketing, grants, or public site: “aligned with Te Mana Raraunga”, “Charter compliant”, “sovereign by design” without named live controls  

**Blockers to L2 (pilot-ready claims):**  
1. Consent + purpose-binding on personal/cultural access  
2. Runtime Sovereignty Gate (fail-closed) on every external model path  
3. HITL L2+ proven on health-adjacent and cultural outputs  
4. Disclaimers + cultural review path documented and exercised  
5. Signed scorecard after evidence links attached  

**Next review:** Before any pilot LOI language or public Hub claim  

---

## Sign-off

Founder / designated authority: _________________ Date: _________  

*Draft only. Health-adjacent + cultural data → fail-closed: no external alignment claim until L2 with evidence.*
