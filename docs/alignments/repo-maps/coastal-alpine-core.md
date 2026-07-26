# Repo Alignment Map — Coastal-Alpine-Core

**Repo**  
https://github.com/fivepanelhat/Coastal-Alpine-Core  

**Role**  
Shared architecture foundation: SecurityGuard, TelemetryTracker, DataFlywheel, SovereignOllamaClient, portal_core for RPi 5 + Hailo-10H.

---

## Primary Alignments

| Instrument / Source | Strength | Notes |
|---------------------|----------|-------|
| Te Mana Raraunga | Strong | Local-first, owner-influenced keys, no silent exfiltration, data flywheel under sovereignty rules |
| NZ AI Strategy | Strong | Application focus + responsible controls |
| Algorithm Charter | Medium–Strong | Transparency via telemetry + audit; human oversight via SecurityGuard + HITL upstream |
| Local-first / edge | Strong | Core design premise |

---

## Reinforcement

1. Te Mana Raraunga principles + Te Kāhui Raraunga AI Governance  
2. Hardened NZ AI Safety Guidelines (Aether) — inherited by Core consumers

---

## Gaps / Next Actions

- Explicit consent-graph and runtime sovereignty gate interfaces should surface here or in Weaver
- Document which Core components implement which Minimum Viable Set controls
