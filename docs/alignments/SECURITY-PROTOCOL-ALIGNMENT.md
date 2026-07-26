# Security Protocol Alignment

**Purpose**  
Connect the alignments evidence library to CAT / Aether security protocols so that sovereignty, compliance, and security controls are coherent and fail-closed.

**Status**  
Draft — Alignment Week (July 2026). Local only until reviewed.

---

## 1. Existing Security Instruments

| Instrument | Location | Role |
|------------|----------|------|
| **SECURITY.md** | Aether root | Vulnerability disclosure, built-in controls, fleet security principles |
| **SecurityGuard** | Coastal-Alpine-Core | Input/output screening, injection defence, tenant isolation, capability gating |
| **ThreatModeler + Guardrails** | Aether | Gate high-risk tools to HITL |
| **Hardened NZ AI Safety Guidelines** | `docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md` | Fail-closed, least privilege, local-first, HITL |
| **COMPLIANCE.md** | Aether root | Privacy, Te Mana Raraunga, no data sales, HITL |
| **Security skills** | Aether skills | Route audit, error-message sanitisation, schema enforcement, notifications triage, Te Mana Raraunga sovereignty |
| **Runtime Sovereignty Gate** (experimental) | Local `te-mana-raraunga-controls` | Pre-flight check before off-box / external-model transfer |

---

## 2. Security Principles (unified)

These are already stated across SECURITY.md, COMPLIANCE.md, and the Hardened Guidelines. Alignments treat them as non-negotiable:

1. **No silent exfiltration** of personal, tenant, or culturally sensitive data  
2. **Local-first** processing; third-party AI only with explicit configuration and disclosure  
3. **Least privilege** and capability gating (SecurityGuard / Guardrails)  
4. **Fail-closed** — if a required check cannot be completed, block the action  
5. **HITL for high-stakes** — production writes, external actions, health/cultural content, key/consent/location changes  
6. **Owner-controlled credentials and keys** where sensitivity requires it  
7. **No sale of personal or customer operational data**  
8. **Transparency of AI processing** — no silent training on private content without consent  

---

## 3. How alignments reinforce security

| Alignments area | Security contribution |
|-----------------|------------------------|
| **Te Mana Raraunga controls** | Runtime Sovereignty Gate, consent checks, encryption + key control, provenance — all reduce exfiltration and unauthorised use |
| **NZ government instruments** | Algorithm Charter human oversight + transparency; Privacy Act purpose limitation and notification duties |
| **International production (routing / CPST)** | Cost-aware routing must never bypass sensitivity or sovereignty checks; cheaper paths still pass SecurityGuard |
| **Repo maps** | Each high-stakes repo (especially Front_Line_Whanau) inherits the same security + HITL baseline |

Security is not a separate silo. Sovereignty controls *are* security controls when data is taonga or personal.

---

## 4. Security ↔ Sovereignty control mapping

| Security concern | Primary control | Alignments reference |
|------------------|-----------------|----------------------|
| Data leaving the boundary | Runtime Sovereignty Gate + no silent exfil | `te-mana-raraunga/operational-controls.md` |
| Unauthorised model / tool use | SecurityGuard + Guardrails + HITL | Hardened Guidelines + SECURITY.md |
| Prompt injection / tool abuse | SecurityGuard input screening | Core + security skills |
| Tenant isolation | Strict partitioning of stores / memory | COMPLIANCE.md + Core |
| Credential / key exposure | Owner-influenced keys, least privilege | Te Mana Raraunga R3 + Core |
| Hallucinated high-stakes output | Grounding, verification, HITL | Hardened Guidelines + anti-hallucination (CAT_CONGRUENCE) |
| Supply-chain / dependency risk | Dependabot, pinned versions, CI | SECURITY.md |

---

## 5. Required behaviour for any external or high-impact path

Before an agent or system may:

- Call an external model  
- Transfer data off the edge / NZ-resident boundary  
- Actuate a real-world control  
- Touch personal, health, or Māori data  

It must satisfy:

1. SecurityGuard (or equivalent) screening  
2. Sensitivity / classification check  
3. Consent check where personal or cultural data is involved  
4. Runtime Sovereignty Gate decision (fail-closed)  
5. HITL approval when the gate or policy requires it (default L2+ for production / health / cultural / external)  

Cost, latency, or convenience ranking is subordinate to the above.

---

## 6. Alignment Week security checklist

- [ ] Confirm SECURITY.md fleet principles remain the public baseline  
- [ ] Ensure experimental Runtime Sovereignty Gate is documented as complementary, not replacing SecurityGuard  
- [ ] Front_Line_Whanau and any health-adjacent paths explicitly inherit L2+ + cultural review  
- [ ] Routing skill (when used) never escalates restricted/taonga content on cost alone  
- [ ] No new external claim of “secure” or “sovereign” without the controls above being present  
- [ ] Vulnerability disclosure path (GitHub Security Advisory) remains the only public reporting channel  

---

## 7. Promotion notes

When alignments are promoted:

- Add a short “Security Protocol Alignment” pointer in SECURITY.md (see `proposed-inserts.md` for pattern)  
- Keep SecurityGuard + ThreatModeler + Guardrails as the runtime enforcement layer  
- Treat the Runtime Sovereignty Gate as the sovereignty-specific pre-flight that sits alongside (not instead of) SecurityGuard  

---

**Owner**  
Coastal Alpine Tech  

**Related**  
- `Aether/SECURITY.md`  
- `Aether/docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md`  
- `Aether/COMPLIANCE.md`  
- `alignments/GOVERNANCE-COMPLIANCE-TRUST.md`  
- Experimental: `te-mana-raraunga-controls` (Runtime Sovereignty Gate)
