# Trust Hub — [Product Name]

**For pilot partners, iwi, and early adopters:** This is how [Product Name] works, what it won't do, and how we've built trust into every layer.

---

## The One-Minute Version

[Product Name] is a [type of AI] that helps [primary use case]. It runs on your device by default — nothing leaves unless you explicitly approve it. A human reviews every major decision before it affects you. Your data is encrypted, stays in Aotearoa, and you can delete it anytime.

**Bottom line:** You stay in control. We make the technology transparent so you can make informed choices.

---

## What [Product Name] Does

[Clear description of capabilities, in plain language. Example:]

"[Product Name] analyzes soil sensor data and suggests when to apply fertilizer. It learns from your field over time — the longer you use it, the more tailored the recommendations become. It factors in weather, your crop type, and local soil conditions."

**What it does NOT do:**
- [Example: We do not control fertigation systems automatically]
- [Example: We do not collect or use GPS location data]
- [Example: We do not share your data with other farmers or third parties]
- [Example: We do not make decisions without human review]

---

## How We Keep Your Data Sovereign

### Layer 1: Offline by Default
The AI runs on your device. Your data never leaves unless you ask.

**How we enforce this:**
- [Technical detail: e.g., "Ollama + Hailo-10H inference on Raspberry Pi 5, no cloud round-trip"]
- Code review requirement: any data transmission must be approved by engineering lead + privacy officer
- Automated test: every release verifies offline mode works without network
- **You can verify:** Disconnect your device from WiFi and the AI still works

### Layer 2: Explicit Consent
If you choose to share data (e.g., for analysis), you approve it each time.

**How we enforce this:**
- [Technical detail: e.g., "Consent dialog in UI before any transmission; user fingerprint/PIN required"]
- No "send everything automatically" setting in production
- Consent logged: timestamp, what data, what for, who approved it
- **You can verify:** Check Settings → Data → Sent & Shared History; every entry has a date and approval record

### Layer 3: Encryption in Transit
Data moving from your device is locked (AES-256 encryption).

**How we enforce this:**
- [Technical detail: e.g., "TLS 1.3+ on all API endpoints; certificate pinning to prevent man-in-the-middle"]
- Code review: any credential or API call flagged in security scan
- Automated test: monthly verification that encryption is active
- **You can verify:** Network packet inspection shows `https://` and certificate validity

### Layer 4: Data Stays in Aotearoa
Your data is stored only in New Zealand data centers.

**How we enforce this:**
- [Technical detail: e.g., "AWS Aotearoa region (ap-southeast-2) only; replication to backup DC in Hamilton"]
- Compliance audit: quarterly confirmation no data replicated internationally
- Legal contract: hosting provider contractually prohibited from moving data out of Aotearoa
- **You can verify:** Ask us for the hosting agreement or SOC 2 audit report

### Layer 5: You Control Deletion
You can delete your data anytime. We verify it's gone.

**How we enforce this:**
- [Technical detail: e.g., "Data deletion API call triggers immediate purge from active DB + backup queues"]
- Deletion confirmed: we send you a deletion receipt within 24 hours
- Retention exception: health data kept 7 years per NZ Privacy Code (we'll anonymize after use is done)
- **You can verify:** Delete data via UI, then ask us for proof it's gone; we'll provide a signed deletion log

---

## Human-in-the-Loop: You Stay in Control

**Every significant decision has a human approval gate.**

Example workflow:
1. AI analyzes your data: "High nitrogen levels detected"
2. AI recommends: "Hold fertilizer for 2 weeks"
3. **Human agronomist reviews** the data and recommendation
4. **You see and approve** before anything happens
5. You can accept, modify, or reject the recommendation
6. The decision is logged (who, what, when, why)

**No automatic actions.** The AI never:
- Changes your device settings without your approval
- Triggers physical actuators (fertigation, dosing, etc.) without a human-confirmed button press
- Modifies data without logging the change
- Sends data off-device without your explicit consent

**Audit trail:** Every decision is logged. You can request a copy anytime.

---

## Transparency & Accountability

### What We Measure
- **Uptime:** [e.g., 99.5% monthly availability; public dashboard at status.example.nz]
- **Accuracy:** [e.g., fertilizer recommendations within 10% of agronomist recommendations; monthly audit]
- **Fairness:** [e.g., recommendation accuracy equal across field sizes, soil types; quarterly bias audit]
- **Response time:** [e.g., analysis completes within 30 seconds; monitored continuously]

### Public Artefacts
- **[Changelog](link):** Every update, what changed, why
- **[Privacy Notice](link):** Full legal terms
- **[SOC 2 Audit Report](link):** Independent security assessment (annual)
- **[Incident Log](link):** Any data breach or outage, what happened, how we fixed it
- **[Model Fairness Report](link):** Bias detection results, demographic parity scores (quarterly)

### How We Learn & Improve
- **Feedback loop:** We collect user feedback on recommendation quality
- **Monthly retraining:** The AI improves based on your data + feedback
- **Fairness audits:** Monthly check for bias; if detected, we pause updates and investigate
- **You're told:** Every month, you see "Model updated — here's what changed"

---

## Community Trust: How We Earn It

### For Iwi & Hapū
- **Te Mana Raraunga principles:** Data ownership, control, and access governed by iwi, not by us
- **Cultural Advisory Board:** Iwi leadership reviews any use of cultural or health data
- **Dual-key encryption:** Iwi holds one key; we hold another; both needed to decrypt
- **Data use agreement:** Signed by iwi leadership; we follow it or we lose the privilege
- **Benefit-sharing:** [Specific commitment, e.g., "10% of revenue from this product reinvested in iwi-led AI projects"]

### For Farmers / Clinic Managers
- **Local business:** We're here to stay, not VC-backed churn
- **Direct contact:** You can reach a human (not a bot) within 24 hours
- **Annual review:** We sit down with you once a year — how's it working? What would you change?
- **Transparent pricing:** What you pay, and what you get, no surprises
- **Exit path:** You can leave anytime; we'll hand you all your data in a portable format

### For Everyone
- **Honest about limits:** We tell you what the AI can't do as clearly as what it can
- **No hype:** We don't claim "AI magic" or "autonomous farming"; we say "AI-assisted decision-making with human oversight"
- **Incident honesty:** If something goes wrong, we tell you immediately, explain why, and what we're doing about it
- **No vendor lock-in:** Your data is yours; you can export it and move to a different tool if you want

---

## Common Questions

**Q: What if the AI makes a wrong recommendation?**

A: The human agronomist catches most errors before you see them. If one gets through and you follow it, that's data for us to improve. But here's the thing: the AI is not the decision-maker — you are. We're a tool that helps you decide faster, not replaces your judgment.

**Q: Can you use my data to train a model you sell to someone else?**

A: No. Your data improves *your* local model only (the one on your device). If we ever wanted to train a general model, we'd ask your explicit permission and offer compensation. That's not our current plan, but if it changes, we'll tell you.

**Q: What if you get hacked?**

A: Unlikely (we invest heavily in security), but if it happens: you'll know within 24 hours. We'll explain what was accessed, what we're doing to fix it, and what you should do (e.g., monitor your accounts). We'll offer support (credit monitoring, legal help, etc.). We'll file a report with the Privacy Commissioner. And we'll change our practices so it doesn't happen again.

**Q: Can you promise my data will never leave Aotearoa?**

A: Yes — and we've written it into our hosting contracts. If we ever want to change that, we'll ask your permission first. If you say no, we delete the data or shut down the product; we don't override your choice.

**Q: How long do you keep my data?**

A: Only as long as you use the product. When you delete your account, we delete the data (except health data, which we keep 7 years per NZ law, then anonymize). You can verify deletion.

**Q: Who reviews the AI recommendations?**

A: [Specific role, e.g., licensed agronomist, registered health professional, certified data analyst]. They're trained in both the technology and the domain (farming / health / etc.). They have a conflict-of-interest policy: they can't benefit from bad recommendations. Reviews are logged and auditable.

---

## How to Reach Us

**Questions about data:**  
📧 privacy@[company].nz | ☎️ [phone] | 🕐 [hours]

**Questions about how to use [Product Name]:**  
📧 support@[company].nz | 💬 In-app chat | 📞 [phone]

**Concerns about trust or recommendations:**  
Contact [Name], Chief Trust Officer  
📧 trust@[company].nz | ☎️ [direct line]

**Privacy complaint (if we don't respond):**  
Privacy Commissioner | https://www.privacy.org.nz/ | 0800 803 202

---

## Governance & Oversight

**This product is built on:**
- NZ Privacy Act 2020 (all 11 Information Privacy Principles)
- Te Mana Raraunga (Māori data sovereignty framework)
- CAT Architectural Standards (Coastal Alpine Tech's tiered security model)
- MBIE Responsible AI Framework (explainability, fairness, safety-by-design)
- SOC 2 Type II compliance (independent security audit)

**Who oversees us:**
- Internal: Privacy Officer, CISO, Cultural Advisory Board, Product Lead
- External: SOC 2 auditor (annual), Privacy Commissioner (if you file a complaint)

**You can request:**
- Audit report (SOC 2 Type II) — ask privacy@[company].nz
- Data governance documentation — ask privacy@[company].nz
- Fairness audit results — available at [product dashboard]
- Cultural Advisory Board meeting minutes (anonymized) — ask trust@[company].nz

---

## Pilot Agreement

If you're considering a pilot:

1. **We provide:**
   - Free access to [Product Name] for pilot period
   - Direct support (phone/email within 4 hours)
   - Monthly check-ins to review progress
   - This Trust Hub + Data Card (no changes mid-pilot)

2. **You commit to:**
   - Feedback: tell us what's working and what isn't
   - Data access: allow us to audit your usage patterns (anonymized)
   - Transparency: you can share our Trust Hub with other farmers/clinics

3. **Data during pilot:**
   - Stays in Aotearoa, encrypted, under your control
   - Deleted when pilot ends, or you keep it (your choice)
   - Not used for marketing ("Case study: farmer X grew 20% more…" only with your permission)

4. **If it's not working:**
   - You can exit anytime, no penalty
   - We delete your data on request
   - We'll ask what went wrong so we can improve

---

## Version & Commitment

**Trust Hub version:** [X.Y.Z]  
**Effective date:** [date]  
**Next review:** [date]

**Our commitment:** This Trust Hub reflects how [Product Name] actually works today. If we change how we handle data or make decisions, we'll update this document and tell you what changed. You'll never wake up to find we've quietly changed the rules.

---

**Last updated:** [date]  
**Approved by:** Privacy Officer + Chief Trust Officer + [Cultural Advisory Board, if applicable]  
**Public:** Yes (share this with anyone considering using or partnering with [Product Name])
