# cat-egress-sentinel — Changelog

All notable changes to this skill are documented here.  
Versioning follows Semantic Versioning (MAJOR.MINOR.PATCH).

## [0.2.0] — 2026-07-18

### Added
- Initial draft of the context-aware data-egress sentinel.
- Static scanner that classifies dependencies RED / AMBER / GREEN by context.
- HITL-gated runtime probe that observes connection metadata only (never payloads).
- Report-first posture: blocking and allowlist changes require explicit human approval.

### Notes
- Status: draft. Pending skills-ci, pytest, and live node test.
- Cultural review of Te Mana Raraunga content required before v1.0.0.
