# Hash-Anchor Runbook — Phase 1 (Trust-only)

**Skill:** aether-web3-trust-layer  
**Phase:** 1 — Anchoring only (no tokens, no public liquidity)  
**Claim tier:** L1 Designed  
**Last updated:** 2026-08-04

## Purpose

Produce an immutable *pointer* to an off-chain audit or compliance artefact without putting operational or personal data on-chain.

## When to use

- Night Cycle evening summary pack
- Node / farm daily operational summary (aggregates only)
- Skill or release evidence pack
- Consent-grant or policy-change receipt (metadata only)

## When not to use

- Raw sensor streams, GPS traces, or whānau health content
- Anything lacking a consent-graph check for the data class
- As a substitute for local backup or owner-controlled keys

## Procedure (offline-first)

### 1. Prepare the artefact (local)

1. Collect the pack under an owner-controlled path.
2. Strip or avoid PII, farm identifiers in clear text, and health detail.
3. Prefer aggregates, hashes of source files, and structured metadata.
4. Write a short manifest listing artefact_id, created_at, producer, content_sha256, sensitivity_class, consent_ref.

### 2. Canonicalise and hash

```bash
find ARTIFACT_DIR -type f | sort | cpio -o 2>/dev/null | sha256sum
sha256sum path/to/pack.tar.gz
```

### 3. Sign locally (edge)

- Sign the final manifest hash with the node or organisation key under owner control.
- Do not paste private keys into agent context.
- Agents may prepare the unsigned payload; humans approve signing.

### 4. Optional chain anchor (testnet first)

Only after HITL L2 approval: minimal on-chain object (Sui) or Walrus blob with content hash, timestamp, optional pointer URI. Prefer testnet. Record tx digest locally.

### 5. Verify

Recompute hash; match manifest. If anchored, confirm on-chain hash equality.

## HITL

| Step | Gate |
|------|------|
| Prepare local pack | L0–L1 |
| Sign with org/node key | L2 |
| Submit testnet anchor | L2 |
| Submit mainnet anchor | L2 (prefer L3) |
| Public claim anchored on Sui | L2 + evidence |

## Success criteria

- Local pack reproducible; SHA-256 verified
- No forbidden data classes in clear text
- Consent/sensitivity noted
- If on-chain: testnet unless pilot approved

## Failure modes

- Hash mismatch → new artefact; do not silently overwrite
- Missing consent for restricted class → do not anchor
- Agent requests key material → hard refuse
