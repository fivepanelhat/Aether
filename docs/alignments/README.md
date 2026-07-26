# Alignments — Coastal Alpine Tech / Aether / Kiwi Edge

**Purpose**  
Single source of truth for how CAT systems align with New Zealand government instruments, Te Mana Raraunga principles, and high-signal international production evidence.

**Status**  
Draft for Alignment Week (late July 2026). Local only until reviewed and promoted.

**How to use**
1. Start with the relevant `repo-maps/` file for the system you are working on.
2. Follow links into the detailed instrument or principle files.
3. Cite the external sources (not internal summaries) in grants, ADRs, pilot agreements, and public claims.
4. Treat any claim of “alignment” as requiring concrete technical + governance evidence (see anti-patterns in the Hardened NZ AI Safety Guidelines).

**Structure**

```
alignments/
├── README.md
├── GOVERNANCE-COMPLIANCE-TRUST.md     ← authority stack + Trust Protocol
├── SECURITY-PROTOCOL-ALIGNMENT.md     ← security ↔ sovereignty mapping
├── proposed-inserts.md                ← draft text for COMPLIANCE / CAT_CONGRUENCE / SECURITY
├── nz-government/
│   ├── nz-ai-strategy.md
│   ├── algorithm-charter.md
│   └── public-service-ai-framework.md
├── te-mana-raraunga/
│   ├── principles.md
│   ├── te-kahui-raraunga-ai-governance.md
│   └── operational-controls.md
├── international-production/
│   ├── agent-performance-cpst.md
│   ├── model-routing.md
│   └── harness-and-skills.md
└── repo-maps/
    ├── aether.md
    ├── coastal-alpine-core.md
    ├── weaver.md
    ├── front-line-whanau.md
    ├── byte-size-kai.md
    └── edge-firmware-and-portals.md
```

**Ownership**  
Coastal Alpine Tech. Material changes require founder review.

**Governance & security integration**  
- `GOVERNANCE-COMPLIANCE-TRUST.md` — authority stack, Trust Protocol, claim discipline  
- `SECURITY-PROTOCOL-ALIGNMENT.md` — SecurityGuard / ThreatModeler / HITL / sovereignty gate mapping  
- `proposed-inserts.md` — draft paragraphs for COMPLIANCE.md, CAT_CONGRUENCE.md, SECURITY.md  

**Related existing artefacts**
- `Aether/docs/HARDENED_NZ_AI_SAFETY_GUIDELINES.md` (primary hardening of NZ instruments)
- `Aether/COMPLIANCE.md` + `CAT_CONGRUENCE.md` + `SECURITY.md`
- `skills/aether-nz-ai-safety`
- `skills/te-mana-raraunga-sovereignty` (existing lighter skill)
- Local experimental skills: `te-mana-raraunga-controls`, `aether-agent-performance`, `aether-agent-routing`
