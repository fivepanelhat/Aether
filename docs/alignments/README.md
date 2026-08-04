# Alignments — Coastal Alpine Tech / Aether / Kiwi Edge

**Purpose**  
Single source of truth for how CAT systems align with New Zealand government instruments, Te Mana Raraunga principles, and high-signal international production evidence.

**Status**  
On `main` (PR #37). Metrics hardening added 27 July 2026.

**How to use**
1. Start with the relevant `repo-maps/` file for the system you are working on.
2. Follow links into the detailed instrument or principle files.
3. Cite the external sources (not internal summaries) in grants, ADRs, pilot agreements, and public claims.
4. Treat any claim of “alignment” as requiring concrete technical + governance evidence.
5. **Before any external claim:** run `ALIGNMENT-METRICS.md` scorecard; overall Fail blocks the claim language.

**Structure**

```
alignments/
├── README.md
├── ALIGNMENT-METRICS.md               ← scorecard, tiers L0–L4, metric families
├── GOVERNANCE-COMPLIANCE-TRUST.md
├── SECURITY-PROTOCOL-ALIGNMENT.md
├── proposed-inserts.md
├── scorecards/
│   └── TEMPLATE.md
├── nz-government/
├── te-mana-raraunga/
├── international-production/
└── repo-maps/
```

**Ownership**  
Coastal Alpine Tech. Material changes require founder review.

**Governance, security & metrics**  
- `ALIGNMENT-METRICS.md` — measurable Pass/Fail families; claim language bound to tier  
- `GOVERNANCE-COMPLIANCE-TRUST.md` — authority stack, Trust Protocol  
- `SECURITY-PROTOCOL-ALIGNMENT.md` — SecurityGuard / HITL / sovereignty gate mapping  
- `scorecards/TEMPLATE.md` — copy per repo before pilot or public claim  
- `proposed-inserts.md` — draft paragraphs for COMPLIANCE / CAT_CONGRUENCE / SECURITY  

**Related existing artefacts**
- `Aether/docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md` (primary hardening of NZ instruments)
- `Aether/COMPLIANCE.md` + `CAT_CONGRUENCE.md` + `SECURITY.md`
- `skills/aether-nz-ai-safety`
- `skills/te-mana-raraunga-sovereignty` (existing lighter skill)
- Local experimental skills: `te-mana-raraunga-controls`, `aether-agent-performance`, `aether-agent-routing`
