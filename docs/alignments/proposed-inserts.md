# Proposed Inserts — COMPLIANCE.md & CAT_CONGRUENCE.md

These are **draft paragraphs only**. They are not applied to the live repo. Use them when the alignments tree is promoted.

---

## 1. Proposed insert for COMPLIANCE.md

Place after the fleet mandatory block (or under a new “Alignment Evidence” heading):

```markdown
## Alignment Evidence

Detailed mapping of Aether and the wider Kiwi Edge stack to external instruments is maintained in the alignments library:

- New Zealand government instruments (AI Strategy, Algorithm Charter, Public Service AI Framework)
- Te Mana Raraunga principles and Te Kāhui Raraunga Māori AI Governance Framework
- International production evidence (agent performance, cost-per-successful-task, model routing, harness design)

See `docs/alignments/` (or the current path of the alignments tree).

The alignments library is **evidence and mapping only**. Binding controls remain those stated in this document and in the Hardened NZ AI Safety Guidelines. External claims of alignment require concrete controls plus founder approval.
```

---

## 2. Proposed insert for CAT_CONGRUENCE.md

Place under the existing “NZ AI Safety (hardened)” section:

```markdown
### Alignment evidence library

Repo-level and instrument-level mapping lives in the alignments library (`docs/alignments/` or equivalent). It covers:

- NZ government strategy and Charter commitments
- Te Mana Raraunga operational controls
- International production sources used for performance, routing, and skills architecture

Use the relevant `repo-maps/*.md` file when preparing grants, pilot language, or public claims. Alignments do not replace the Hardened Guidelines or the autonomy ceiling in this document.
```

---

## 3. One-line README pointer (high-stakes repos)

```markdown
**Alignment map:** see `docs/alignments/repo-maps/<repo-name>.md` for how this system maps to NZ AI Strategy, Algorithm Charter, and Te Mana Raraunga.
```

---

These inserts keep governance, compliance, and trust protocols as the authority while making the alignments library the traceable evidence layer.

---

## 4. Proposed insert for SECURITY.md

Place under “Fleet security principles” or as a short new section:

```markdown
## Alignment with sovereignty & NZ instruments

Security controls are designed to operate together with Te Mana Raraunga principles and the Hardened NZ AI Safety Guidelines. In particular:

- No silent exfiltration and local-first defaults support Kaitiakitanga and Rangatiratanga.
- HITL gates for high-stakes and culturally sensitive actions align with the Algorithm Charter spirit and Public Service AI expectations.
- Detailed mapping lives in the alignments library (`docs/alignments/` or equivalent), including the Security Protocol Alignment note.

Runtime enforcement remains SecurityGuard, ThreatModeler/Guardrails, and HITL. Alignments provide evidence and mapping only.
```
