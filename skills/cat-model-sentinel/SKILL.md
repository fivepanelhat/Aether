---
name: cat-model-sentinel
description: Baseline-and-check monitor for edge model availability, latency, integrity and behavioural drift.
license: MIT
compatibility: aether-0.5+
allowed-tools: [bash, python, read_file]

metadata:
  version: 0.1.0
  status: draft
  type: sentinel
  category: model-ops
  requires_hitl: false
  related_skills: [te-mana-raraunga-sovereignty]
  tags: [model-health, drift-detection, integrity, ollama, edge]
  changelog: |
    v0.1.0 (draft) - Pluggable backends + silent swap detection + cultural-canary. Passes validate-skill.sh.
---

# cat-model-sentinel

Model health & drift monitor for sovereign edge deployments.

## Core Behaviour
- Tracks model digest + tag pinning
- Detects silent swaps (e.g. gemma4:latest replacing pinned version) as RED
- Pluggable backends: ollama, mock (validated), yolo
- Cultural-canary drift escalates to cultural review

Status: draft. Comparison engine validated via mock backend.
