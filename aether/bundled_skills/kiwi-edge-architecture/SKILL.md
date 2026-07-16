---
name: kiwi-edge-architecture
description: Applies the Kiwi Edge AI Stack system map when working on Coastal Alpine repos — field firmware, mTLS MQTT, Core SDK, Weaver, domain portals, Ollama + Hailo-10H on RPi 5 16GB, SecOps, and data flywheel.
version: "1.0.0"
type: orchestration
requires_hitl: false
cultural_sensitivity: high
tags: [architecture, kiwi-edge, coastal-alpine, raspberry-pi, hailo, ollama, mqtt]
---

# Kiwi Edge Architecture

## Overview
Encodes the **July 2026** Coastal Alpine / Kiwi Edge system map so Aether plans changes against the correct layer instead of treating every repo as a generic web app.

**Canonical hardware:** Raspberry Pi 5 **16GB** + **Hailo-10H** (40 TOPS). Local LLM: Ollama (`gemma4:e4b` / coder models for Aether).

## When to Use
- Working in `coastal-alpine-stack`, `Coastal-Alpine-Core`, `Weaver`, portals, firmware, or this Aether companion
- Scaffolding or refactoring that must respect edge offline / sovereignty constraints
- Updating architecture diagrams, README system maps, or repo blurbs

## Instructions

### 1. Identify the plane
| Plane | Repos / components | Do not break |
| ----- | ------------------ | ------------ |
| Field | Sovereign-Edge-Firmware, ESP32 sensors | mTLS client identity, offline-first |
| Fabric | Mosquitto mTLS :8883, ACLs, nftables | Topic isolation, no cleartext secrets |
| SDK | Coastal-Alpine-Core | `SecurityGuard`, telemetry, flywheel, portal_core contracts |
| Orchestration | Weaver | Multi-tenant routing, RAG locality |
| Portals | AquaGuard, SoilGuard, Blue-Moon, Sting | Domain agents + actuator fail-closed |
| AI | Ollama + Hailo-10H | Local inference only |
| Trust | HITL, SecOps CI, Dependabot, Prometheus | Least-privilege Actions tokens |

### 2. Prefer Core SDK primitives
- Prompt/input checks → `SecurityGuard` / `input_guard_check` (Core ≥0.5.4 patterns)
- Trajectories → `DataFlywheel` (never commit `flywheel_*.jsonl`)
- LLM calls → `SovereignOllamaClient` edge defaults
- Portal loops → `portal_core` AIAgent / MQTT / AV / HardwareController

### 3. Control loop (portals)
`sensors/MQTT → analyze → SecurityGuard → plan → enforce → flywheel outcome → audit`

### 4. Docs & blurbs
When updating public architecture copy:
- Keep RPi 5 16GB + Hailo-10H consistent (no Hailo-8 / 8GB SKUs)
- Link monorepo maps: stack `README.md` / `ARCHITECTURE.md`, landing `fivepanelhat` portfolio
- Core NZ regulations for Core/stack/firmware/Aether: **Te Mana Raraunga 2018**

## Guardrails & Constraints
- Do not introduce cloud-only dependencies for inference or telemetry buses
- ChromaDB: localhost-only until upstream GHSA-f4j7 is patched
- Workflow YAML must declare least-privilege `permissions:` (default `contents: read`)
- Cultural sensitivity: data generated on whenua stays under local custody

## References
- `fivepanelhat` portfolio + architecture map
- `coastal-alpine-stack/ARCHITECTURE.md`
- `Coastal-Alpine-Core` SECURITY.md (threat register)
- Related skills: `security-notifications-triage`, `te-mana-raraunga-sovereignty`, `build-ci-hygiene`
