# Repo Alignment Map — Edge Firmware & Domain Portals

**Repos covered**
- Sovereign-Edge-Firmware  
- SoilGuard-Portal  
- AquaGuard-Portal  
- Sting-Operation-AI  
- coastal-alpine-stack (monorepo view)

**Role**  
Field layer (ESP32 / sensors) → mTLS MQTT → Core → domain portals. Offline-by-design, primary-industry focus.

---

## Primary Alignments

| Instrument / Source | Strength | Notes |
|---------------------|----------|-------|
| Te Mana Raraunga / Kaitiakitanga | Strong | Whenua, water, biosecurity data; local control |
| Local-first / NZ residency | Strong | Offline-by-design, edge inference |
| NZ AI Strategy | Strong | Application in primary industries |
| Fail-closed / least privilege | Strong | SecurityGuard + hardware constraints |

---

## Reinforcement

1. Te Mana Raraunga principles  
2. Hardened NZ AI Safety Guidelines (local-first, no silent exfiltration)

---

## Gaps / Next Actions

- Explicit sensitivity classification for sensor streams
- Clear rules for which aggregated signals may leave the farm / edge node
- Provenance on any derived models or alerts that affect decisions
