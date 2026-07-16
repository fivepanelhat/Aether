# Aether v0.6.0 Release Communications

## 1) Short Public Announcement

Aether v0.6.0 is live.

This first public release delivers a safer, more reliable agentic development workflow for founders and small teams. v0.6.0 introduces dynamic skill loading, stronger guardrails for high-risk actions, improved orchestration behavior, and practical examples/documentation for getting started quickly.

Download:
- https://github.com/fivepanelhat/Aether/archive/refs/tags/v0.6.0.zip
- https://github.com/fivepanelhat/Aether/archive/refs/tags/v0.6.0.tar.gz

## 2) Social Post Version

Aether v0.6.0 is out.

First public release with:
- Dynamic skill loading
- Human-in-the-loop guardrails for risky operations
- Improved orchestrator reliability
- Better docs + practical examples

Built for founders and small teams who need speed with strong safety and oversight.

Download: https://github.com/fivepanelhat/Aether/archive/refs/tags/v0.6.0.zip

## 3) Technical Changelog (Maintainer-Friendly)

### Added
- LLM integration module for Ollama-based decisioning support.
- Dynamic skill auto-discovery from the skills directory.
- New workflow skills:
 - git-workflow
 - error-remediation-orchestrator
 - ci-failure-parser
 - notification-responder
 - project-scaffolder
- GitHub webhook support and retry handling.
- Release-focused test coverage for LLM decision parsing, memory behavior, and guardrail logic.

### Changed
- Orchestrator execution flow tightened for better auditability and safer action handling.
- Memory layer moved to append-only JSONL persistence with bounded in-memory retention.
- Input handling shifted to boundary-safe escaping plus injection pattern detection.
- CLI and startup UX improved for first-run clarity.
- Documentation expanded and refreshed (README, Getting Started, architecture, skill guidance).

### Fixed
- Tool call audit logging issues in orchestrator flows.
- Skills directory resolution and startup edge cases.
- Path safety behaviors in file operations.
- Compatibility issues surfaced by smoke and release tests.

### Validation
- Test suite status at release prep: all tests passing.

## 4) Suggested GitHub Release Body

Aether v0.6.0 is the first public release of a sovereign, safety-aware agentic development system for founders and small teams.

Highlights:
- Dynamic skill loading
- Strong human-in-the-loop guardrails
- Improved orchestrator reliability
- JSONL memory durability improvements
- Better onboarding docs and examples

Download:
- ZIP: https://github.com/fivepanelhat/Aether/archive/refs/tags/v0.6.0.zip
- TAR.GZ: https://github.com/fivepanelhat/Aether/archive/refs/tags/v0.6.0.tar.gz
