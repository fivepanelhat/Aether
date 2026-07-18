# cat-model-sentinel — Changelog

All notable changes to this skill are documented here.  
Versioning follows Semantic Versioning (MAJOR.MINOR.PATCH).

## [0.1.0] — 2026-07-18

### Added
- Initial draft of the edge model health & drift sentinel.
- Model digest tracking and tag pinning.
- Silent-swap detection (e.g. a pinned tag replaced by `:latest`) flagged RED.
- Pluggable backends: ollama, mock (validated), yolo.
- Cultural-canary drift escalation to cultural review.

### Notes
- Status: draft. Comparison engine validated via mock backend.
