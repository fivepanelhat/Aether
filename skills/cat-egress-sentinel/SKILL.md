---
name: cat-egress-sentinel
description: Context-aware data-egress monitor enforcing the offline-native sovereignty guarantee that data never leaves the site.
license: MIT
compatibility: aether-0.5+
allowed-tools: [bash, python, read_file, write_file]

metadata:
  version: 0.2.0
  status: draft
  type: sentinel
  category: sovereignty
  cultural_sensitivity: high
  requires_hitl: true
  related_skills: [te-mana-raraunga-sovereignty]
  tags: [data-sovereignty, egress, hitl, edge, offline-first]
  changelog: |
    v0.2.0 (draft) - Static scanner + HITL-gated metadata-only probe. Report-first. Passes validate-skill.sh.
---

# cat-egress-sentinel

Context-aware data-egress monitor for sovereign edge/hub systems.

## Core Behaviour
- Static scanner classifies dependencies RED/AMBER/GREEN by context
- Runtime probe is HITL-gated and only observes connection metadata (never payloads)
- Always report-first. Blocking or allowlist changes require explicit human approval

Status: draft. Pending skills-ci + pytest + live node test.
Cultural review of Te Mana Raraunga content required before v1.0.0.
