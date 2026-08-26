# Algorithm Charter for Aotearoa New Zealand

**Source**  
data.govt.nz (Stats NZ / government data system)  
https://data.govt.nz/use-data/data-ethics/government-algorithm-transparency-and-accountability/algorithmcharter/

**PDF**  
https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-Charter-2020_Final-English-1.pdf

**Nature**  
Non-binding commitment by government agencies to transparency, human oversight, Te Tiriti-consistent partnership, and risk-aware use of algorithms.

**CAT standing**  
Coastal Alpine Tech **acknowledges** the Charter and voluntarily implements its spirit. CAT is not a government agency and is **not a signatory**.

Canonical company acknowledgement: [`GOVERNMENT_ACKNOWLEDGEMENTS.md`](../../../GOVERNMENT_ACKNOWLEDGEMENTS.md)
Public page (landing repo): https://github.com/fivepanelhat/fivepanelhat/blob/main/docs/public/cat-sovereign-governance-layer.md

---

## Six commitments — CAT mapping

| Charter commitment | Official intent | CAT response |
|---|---|---|
| Transparency | Explain how decisions are informed by algorithms | Structured audit trails; plain-English explanation; model version and inference timestamp |
| Partnership | Embed a Te Ao Māori perspective consistent with Te Tiriti | Te Mana Raraunga controls; cultural review on High / Critical paths |
| People | Engage communities and groups affected | Pilot engagement; no silent use of community data |
| Data | Fit for purpose; understand limits; manage bias | Local-first; purpose limitation; provenance; drift monitoring |
| Privacy, ethics and human rights | Peer review; act on unintended consequences | Privacy Act IPPs; Human Rights Act; SecurityGuard-style screening |
| Human oversight | Named contact; appeal path; explain the human role | HITL L2+ default on high-stakes actions; agents draft only |

---

## Risk and AIA

The Charter uses a likelihood × impact matrix. High risk = the Charter must be applied by signatory agencies.

CAT internal equivalent: risk tier Low / Medium / High / Critical mapped to HITL L0–L4. High or Critical production features require AIA-style impact notes before promotion.

AIA user guide: https://data.govt.nz/docs/algorithm-impact-assessment-user-guide

---

## Reinforcement links

1. Charter home — https://data.govt.nz/use-data/data-ethics/government-algorithm-transparency-and-accountability/algorithmcharter/
2. Official PDF — https://data.govt.nz/assets/data-ethics/algorithm/Algorithm-Charter-2020_Final-English-1.pdf
3. Ministry of Justice summary — https://www.justice.govt.nz/justice-sector-policy/key-initiatives/cross-government/the-algorithm-charter/
4. MBIE Responsible AI — humans in the loop — https://www.mbie.govt.nz/business-and-employment/business/support-for-business/responsible-ai-guidance-for-businesses/artificial-intelligence-system-specific-considerations/use-and-outputs

Full pack: `docs/alignments/GRANT-REINFORCEMENT.md`

---

## Claim language

**Allowed:** “Implements the spirit of the Algorithm Charter through explicit HITL and audit trails.”  
**Forbidden:** “Signatory to…”, “Charter certified”, “government approved AI.”

See `docs/alignments/GOVERNANCE-COMPLIANCE-TRUST.md` section 5.
