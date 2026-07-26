# Governance, Compliance & Trust Protocol Bridge

**Purpose**  
Connects the `alignments/` evidence library to the existing CAT / Aether governance, compliance, and trust instruments so that claims are traceable, fail-closed, and reviewable.

**Status**  
Draft — Alignment Week (July 2026). Local only until reviewed.

---

## 1. Authority Stack (order of precedence)

When instruments appear to conflict, apply this order:

1. **Law** — Privacy Act 2020 (incl. IPP 3A), Health Information Privacy Code, sector legislation  
2. **Te Mana Raraunga principles** + Te Kāhui Raraunga Māori AI Governance Framework  
3. **Hardened NZ AI Safety Guidelines** (`docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md`)  
4. **COMPLIANCE.md** + **COMPLIANCE_REGIONS.md**  
5. **CAT_CONGRUENCE.md** (portfolio autonomy ceiling + anti-hallucination)  
6. **alignments/** (this library — evidence and mapping)  
7. Individual skills and runtime behaviour

Alignments never override law or the Hardened Guidelines. They supply the external evidence and repo-level mapping that make the higher instruments concrete.

---

## 2. Trust Protocol (non-negotiable)

| Rule | Statement | Primary evidence |
|------|-----------|------------------|
| **Human authority** | Agents inform, draft, prepare, monitor, remind. Humans advise, decide, sign, file, send, pay. | COMPLIANCE.md §2, CAT_CONGRUENCE.md, HITL protocol |
| **No silent exfiltration** | Data does not leave controlled boundaries without recorded justification and (where required) approval. | Hardened Guidelines, Te Mana Raraunga controls |
| **Local-first default** | Prefer on-device / NZ-resident processing. External models are escalations. | COMPLIANCE.md Core Technical Controls, alignments/te-mana-raraunga |
| **Fail-closed** | If a required sovereignty, consent, or safety check cannot be completed, the action is blocked. | Hardened Guidelines, Runtime Sovereignty Gate |
| **Claim discipline** | Any external claim of alignment, compliance, or “Te Mana Raraunga / Algorithm Charter aligned” requires concrete controls + founder approval. | COMPLIANCE.md Limitations, CAT_CONGRUENCE.md |
| **No data sales** | Personal and customer operational data is not sold. | COMPLIANCE.md fleet block |
| **Anti-hallucination** | Prefer tools/files over memory; label fact / inference / unknown; refuse when evidence is missing. | CAT_CONGRUENCE.md |

---

## 3. How alignments feed governance

```
External instrument (NZ Strategy, Charter, Te Mana Raraunga, Factory evidence…)
        ↓
alignments/  (mapping + reinforcement links + repo impact)
        ↓
Hardened NZ AI Safety Guidelines  (mandatory controls)
        ↓
COMPLIANCE.md  (public-facing commitments)
        ↓
Runtime (HITL gates, SecurityGuard, sovereignty gate, skills)
```

- **alignments/** = evidence and traceability layer  
- **Hardened Guidelines** = enforceable controls  
- **COMPLIANCE.md** = what we are prepared to state externally  
- **Runtime** = what the system actually does

---

## 4. Required cross-references (to be added on promotion)

When the alignments tree is promoted into the Aether repo (or a shared docs location), the following links should be added:

| Existing document | Add |
|-------------------|-----|
| `COMPLIANCE.md` | Short section “Alignment Evidence” pointing to `docs/alignments/` (or equivalent path) |
| `CAT_CONGRUENCE.md` | Reference to alignments under NZ AI Safety / Hardened Guidelines |
| `docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md` | Link to `alignments/te-mana-raraunga/` and `alignments/nz-government/` for source instruments |
| Repo READMEs (high-stakes) | One-line pointer to the relevant `repo-maps/*.md` file |

---

## 5. Trust claims — allowed vs forbidden language

**Allowed (with evidence)**  
- “Designed in accordance with Te Mana Raraunga principles”  
- “Implements the spirit of the Algorithm Charter through explicit HITL and audit trails”  
- “Aligned with the NZ AI Strategy’s responsible adoption posture”  
- “Uses cost-per-successful-task and routing evidence from [named sources]”

**Forbidden without formal review + founder approval**  
- “Fully compliant with…”  
- “Certified under…”  
- “Guarantees Māori data sovereignty” (unless specific controls and agreements are in place)  
- Any claim that implies legal or audit certification that has not been obtained

---

## 6. Alignment Week checklist (governance integration)

- [ ] Review this bridge document  
- [ ] Confirm authority stack order  
- [ ] Agree allowed/forbidden claim language  
- [ ] Decide target path in Aether (`docs/alignments/` recommended)  
- [ ] Draft the one-paragraph inserts for COMPLIANCE.md and CAT_CONGRUENCE.md  
- [ ] Ensure Front_Line_Whanau and any health-adjacent paths have explicit L2+ + cultural review notes  
- [ ] Keep all experimental skills marked experimental until measurement evidence exists  

---

**Owner**  
Coastal Alpine Tech  

**Related**  
- `alignments/README.md`  
- `Aether/COMPLIANCE.md`  
- `Aether/CAT_CONGRUENCE.md`  
- `Aether/docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md`  
- Experimental skills: `te-mana-raraunga-controls`, `aether-agent-performance`, `aether-agent-routing`
