# Kotahitanga Investment Strategy — Aether AI Engine

**Repository:** Aether  
**Primary Tier:** PLATINUM (intelligent self-improving systems)  
**Secondary Tier:** DIAMOND (enterprise-grade security + auditing)  
**Role:** AI orchestration + agent coordination + model governance  
**Compliance Baseline:** 87% (target: ≥85% for Platinum tier)  
**Last Updated:** 2026-07-12

---

## Aether's Role in Kotahitanga

Aether is the **central AI intelligence engine** that coordinates autonomous agents across Coastal Alpine Tech. It manages:

1. **Agent Orchestration** — Route tasks to specialized agents (data analysis, health recommendations, community coordination)
2. **Model Governance** — Continuous improvement loop (capture decisions → curate data → fine-tune models → evaluate fairness → hot-swap)
3. **Explainability** — Every decision logged + auditable (why did agent recommend X?)
4. **HITL Gates** — Humans can override autonomous decisions (with logging + post-hoc audit)
5. **Fairness Monitoring** — Detect bias drift (monthly scoring + alerts if fairness deteriorates)

**Platinum Tier Classification Rationale:**
- System learns from every decision (data flywheel: errors → improvements → better decisions)
- Continuous model improvement (monthly retraining on curated data)
- Bias detection + mitigation (fairness audits on every model)
- Local fine-tuning (models trained on community-specific data, owned locally)
- Autonomous decision-making with human override capability

**Diamond Secondary Rationale:**
- All AI decisions logged + immutable (18-month audit trail)
- Security boundary: unauthorized access to model weights = data breach
- Encryption of model artifacts (no unencrypted model files in transit)
- Access control: only authorized personnel can retrain/deploy models

---

## Data Classification in Aether

| Level | Examples | Protection |
|-------|----------|-----------|
| **Level 1 (Public)** | General health recommendations, educational content | Standard API, no special controls |
| **Level 2 (Restricted)** | Personalized health advice (based on user profile), risk predictions | Encryption at rest/transit, RBAC, rate limiting |
| **Level 3 (Sensitive)** | Psychiatric diagnosis, genetic risk assessment, cultural knowledge formalization | Dual-key encryption, iwi approval, audit logging, HITL gate required |

**Key Constraint:** Level 3 data requires **Cultural Advisory Board approval** for model training + deployment.

---

## Compliance Status (Current)

**Overall Score: 87% (196/225 items) — YELLOW (improving)** ⚠️

| Category | Items | Passing | Score | Status |
|----------|-------|---------|-------|--------|
| CC1 (Governance) | 15 | 15 | 100% | ✓ |
| CC6 (Access) | 49 | 45 | 92% | ✓ |
| CC7 (Change/Secrets) | 38 | 34 | 89% | ⚠️ |
| CC9 (Security) | 42 | 38 | 90% | ✓ |
| A (Availability) | 22 | 21 | 95% | ✓ |
| P (Privacy) | 34 | 31 | 91% | ✓ |
| Te Mana Raraunga | 11 | 11 | 100% | ✓ |
| Architecture | 9 | 9 | 100% | ✓ |
| **TOTAL** | **225** | **196** | **87%** | **🟡 YELLOW** |

**Status:** **CAPITAL FREEZE** — Remediation in progress. No new projects until Green (≥85% achieved for Platinum tier, but remediation showing strong progress).

**Gap Analysis:**
- CC7 gaps (4 items): Model artifact signing, model versioning + rollback procedures, fine-tuning audit trail
- P gaps (3 items): Model fairness audit procedures, explainability logging format standardization
- A gaps (1 item): Model serving high availability (multi-region replica)

**Remediation Timeline (Target Green by Aug 31, 2026):**
- Week 1–2: Model artifact signing + versioning (cryptographic signing of model weights)
- Week 3–4: Fairness audit procedures + automation (monthly bias scoring)
- Week 5–6: Explainability logging standardization
- Week 7–8: Model serving HA + disaster recovery

---

## OCAP® Verification Framework for Aether

### Model Ownership & Control

**Ownership:**
- Organization owns base model architecture + training pipeline
- Community owns domain-specific fine-tuned models (trained on community data)
- Community data ownership: all training data is community-generated + community-owned
- Shared ownership of model outcomes (recommendations benefit community)

**Control:**
- Model access: authorized agents only (API keys, RBAC)
- Model updates: require Cultural Advisory Board approval (for Level 3 models)
- Model rollback: community can request rollback within 30 days
- Override authority: humans can override any autonomous decision (with logging)

**Access:**
- All model access logged (who queried model, when, with what input, what output)
- Model queries traced to originating user/agent (audit trail)
- Failed access attempts logged + monitored (unauthorized model access = incident)
- Quarterly access audit: human review of all access patterns

**Possession:**
- Model weights stored encrypted (in Vault or encrypted S3)
- Models executed only on authorized infrastructure (Weaver orchestration + edge devices)
- Model artifacts digitally signed (prevent unauthorized modifications)
- Model versioning: all versions retained (audit trail of model evolution)

---

## Model Governance & Continuous Improvement Loop

**Rule:** Every model must improve with every iteration. If model accuracy stagnates or fairness degrades → stop deployment + investigate.

**Monthly Improvement Cycle:**

```
Week 1: Collect & Curate
  - Extract last month's data: all user interactions + model decisions
  - Anonymize + validate data (remove PII, flag outliers)
  - Label outcomes: was model recommendation helpful? (binary: yes/no)
  - Create training dataset (supervised learning: input → expected output)

Week 2: Train & Evaluate
  - Fine-tune model using LoRA/PEFT (efficient retraining)
  - Evaluate on held-out test set (accuracy metric)
  - Fairness audit: check for bias across demographic groups
    - If accuracy improved ≥2%: proceed
    - If accuracy degraded >1%: investigate + stay on current model
    - If fairness degraded: investigate + stay on current model

Week 3: HITL Review
  - Compliance Officer reviews fairness audit results
  - If model targets sensitive decisions (psychiatric, genetic): Cultural Advisory Board review
  - Decision: deploy new model or stay on current?

Week 4: Deploy (if approved)
  - Compile model for edge accelerators (Hailo-10H) if applicable
  - Sign model artifact with organization key
  - Deploy to staging: A/B test (10% traffic to new model, 90% to old)
  - Monitor for 1 week: compare model recommendations side-by-side
  - If new model better: rollout to 100% (gradual, 20% → 50% → 100%)
  - If new model worse: rollback immediately (revert to old model)
```

---

## Explainability Requirements (Aether's Key Control)

**Rule:** Every model decision must be explainable in plain language (not just "accuracy ±X%").

**Implementation:**

```
Model Recommendation: "User has moderate depression risk (LIME explanation)"

User-Facing Explanation (plain language):
  "We notice you've reported low energy for 3 weeks, which combined with 
   your recent health history, suggests you might be experiencing depression. 
   We recommend you discuss this with your primary care doctor. Here are 
   resources: [links to mental health support]"

Audit Log (technical explanation):
  {
    "timestamp": "2026-07-12T10:15:23Z",
    "model_version": "depression-risk-v3.2",
    "user_id": "anonymized_hash",
    "input_features": {
      "days_low_energy": 21,
      "previous_depression_episode": true,
      "medication_changes": false,
      ...
    },
    "model_output": 0.62,  // 62% depression risk
    "decision_threshold": 0.50,
    "decision": "recommend_evaluation",
    "lime_explanation": [
      ("days_low_energy", +0.15),  // most important feature
      ("previous_episode", +0.12),
      ("sleep_quality", -0.05),    // mitigating factor
      ...
    ],
    "human_override": null,  // no override
    "fairness_audit": {
      "demographic_parity": 0.94,  // 94% similar recommendation rate across groups
      "disparate_impact": 0.98,    // 98% is good (>0.80 is acceptable)
      "status": "pass"
    }
  }
```

**Compliance Goals:**
- MBIE Responsible AI (explainability requirement)
- NZ Algorithm Charter (transparent decision-making)
- Te Mana Raraunga (community understands how their data is used)

---

## Active Kotahitanga Projects Using Aether

| Project ID | Name | Model Type | Status | Compliance |
|------------|------|-----------|--------|-----------|
| KAS-2026-003 | Farm Operations AI | Predictive (crop yield) | ACTIVE | 87% ⚠️ |

**For detailed tracking, see:**
- `.github/investment/CAPITAL_ALLOCATION_TRACKER.md` (updated weekly)

---

## How to Request Agent/Model Deployment

**For Level 1/2 Data (Non-Sensitive):**

1. File GitHub issue (model description + training data + fairness implications)
2. Compliance review (3 days): privacy impact assessment
3. Model training + evaluation (10 days)
4. Explainability review (3 days): can non-technical people understand decision logic?
5. Staging deployment + A/B testing (7 days)
6. Production deployment + monitoring

**For Level 3 Data (Sensitive/Indigenous):**

1. Detailed proposal to Compliance Officer + Cultural Advisor
2. **HITL Gate 1:** Cultural Advisory Board reviews (30-day review, mandatory)
   - Is this model decision culturally appropriate?
   - Does it respect indigenous knowledge systems?
   - Are there unintended harms?
3. **HITL Gate 2:** Fairness audit by external auditor (10 days)
   - Are recommendations equally beneficial across demographic groups?
   - Any disparate impact detected?
4. **HITL Gate 3:** CFO approves budget (5 days)
5. Model training on community-curated data
6. Deployment with HITL gates enforced (humans review every recommendation initially)

**Timeline:** 45–60 days for Level 3 data

---

## Compliance Obligations During Project

**Monthly:**
- ☐ Model accuracy tracking (is model improving or stagnating?)
- ☐ Fairness audit (bias detection running, no significant drift)
- ☐ Override rate monitoring (what % of decisions are humans overriding?)
- ☐ Explainability logging verified (all decisions have audit trail)

**Quarterly:**
- ☐ Full 225-point compliance re-audit
- ☐ Model governance review (versioning, rollback procedures, model lineage)
- ☐ Fairness deep-dive audit (external auditor for Level 3 models)
- ☐ Cultural Advisory Board review (for Māori health data models)

**Red Flags (Immediate Escalation):**
- Model accuracy drops >5% (investigate + rollback)
- Fairness metric degrades (bias detected → automatic model revert)
- Override rate >20% (humans rejecting model decisions consistently → model not useful)
- Explainability gap detected (decision made but can't explain why → serious issue)

---

## Key Governance Controls for Aether

### Model Artifact Signing (Integrity Verification)

**Rule:** Every model weight file must be cryptographically signed (prevent unauthorized modifications).

**Implementation:**
```python
import hmac
import hashlib

# Sign model artifact
def sign_model(model_file: bytes, private_key: bytes) -> str:
    signature = hmac.new(private_key, model_file, hashlib.sha256).hexdigest()
    return f"sha256={signature}"

# Verify model signature before loading
def verify_model(model_file: bytes, signature: str, public_key: bytes) -> bool:
    expected_sig = sign_model(model_file, public_key)  # Reproduce signature
    # Constant-time comparison (prevent timing attacks)
    return hmac.compare_digest(expected_sig, signature)

# Usage: before loading model from disk/network
model_data = load_model_from_disk("model.pkl")
signature = load_signature("model.pkl.sig")
if not verify_model(model_data, signature, public_key):
    raise SecurityError("Model signature verification failed! Model may be tampered.")
    # FAIL CLOSED: do not load untrusted model
```

### Fairness Monitoring (Bias Detection)

**Rule:** Every model must be evaluated for fairness monthly. If bias detected → automatic rollback.

**Implementation:**
```python
def fairness_audit(model, test_data, demographic_column):
    """
    Compute fairness metrics across demographic groups.
    """
    results = {}
    
    for group in test_data[demographic_column].unique():
        group_data = test_data[test_data[demographic_column] == group]
        
        # Recommendation rate: % getting positive recommendation
        recommendation_rate = (model.predict(group_data) == "positive").mean()
        results[group] = recommendation_rate
    
    # Demographic parity: recommendation rate should be similar across groups
    demographic_parity = max(results.values()) / min(results.values())
    
    # Acceptable threshold: 1.25 (25% difference is max allowed)
    if demographic_parity > 1.25:
        logger.error(f"FAIRNESS VIOLATION: demographic_parity={demographic_parity}")
        return "FAIL"  # Trigger model rollback
    
    return "PASS"
```

### Override Authority (HITL Gate)

**Rule:** Humans can override any model decision. Override must be logged + audited.

**Implementation:**
```python
# User sees model recommendation
recommendation = model.predict(user_data)  # e.g., "recommend depression screening"

# User or clinician can override
if human_approves(recommendation):
    log_decision(
        user_id=user_id,
        model_decision=recommendation,
        human_decision=recommendation,  # Same
        override=False,
        timestamp=now()
    )
    execute_recommendation()
else:
    # Human overrides model
    human_decision = get_human_input("What's your decision?")
    log_decision(
        user_id=user_id,
        model_decision=recommendation,
        human_decision=human_decision,  # Different
        override=True,
        timestamp=now(),
        reason=human_reasoning
    )
    execute_decision(human_decision)

# Post-hoc: monthly analysis of override patterns
# If override rate >20%: model not trusted → investigate
# If override rate <5%: model doing well → reward team
```

---

## References

1. **Kotahitanga Investment Strategy:** `.github/investment/KOTAHITANGA_INVESTMENT_STRATEGY.md`
2. **Compliance Audit Checklist:** `.github/compliance/references/COMPLIANCE_AUDIT_CHECKLIST.md`
3. **Te Mana Raraunga:** `.github/compliance/references/TE_MANA_RARAUNGA_PRINCIPLES.md`
4. **Incident Response Playbook:** `.github/compliance/references/INCIDENT_RESPONSE_PLAYBOOK.md`
5. **MBIE Responsible AI:** https://www.mbie.govt.nz/dmsdocument/19433
6. **NZ Algorithm Charter:** https://www.beehive.govt.nz/release/aotearoa-new-zealand-algorithm-charter

---

## Contacts

| Role | Name | Email |
|------|------|-------|
| Data Officer / AI Lead | [Name] | [Email] |
| Compliance Officer | [Name] | [Email] |
| Cultural Advisor | [Name] | [Email] |
| Privacy Officer | [Name] | [Email] |
| Repository Owner | [Name] | [Email] |

---

**Version:** 1.0.0  
**Status:** YELLOW (remediation in progress, capital freeze)  
**Remediation Target:** Green by 2026-08-31
