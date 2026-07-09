# Changelog

All notable changes to Aether will be documented in this file.

## [0.6.3] - 2026-07

### Fixed
- CLI no longer crashes after a successful run (`aether.errors` AttributeError)
- Threat model no longer forces HITL on read-only tools (`file_reader`, `codebase_search`, `memory_query`)
- `auto_remediate` is now honored (authorized batch / webhook mode for high-risk actions)
- Single-sourced version: CLI uses `aether.__version__`
- `file_reader` path sandbox aligned with `file_writer` (blocks traversal + symlinks)
- Webhook signature verification fails closed when `GITHUB_WEBHOOK_SECRET` is unset
  (opt-in dev bypass: `AETHER_WEBHOOK_INSECURE=1`)
- `directory_lister` accepts `directory=` alias used by the LLM / tests
- Deterministic pipeline passes tool-appropriate kwargs (not always `query=goal`)

### Changed
- Optional install extra: `pip install -e ".[webhook]"` (fastapi, uvicorn, tenacity)
- Codebase search skips common binary/build dirs and large files for speed

## [0.6.0] - 2026-07

### Added
- Dynamic Skill Loader (skills are now automatically discovered from the `skills/` directory)
- Git Workflow skill for safe branch creation, committing, and pushing
- Error Remediation Orchestrator skill
- CI Failure Parser skill
- Notification Responder skill
- GitHub Webhook support with retry logic
- Project Scaffolder skill (first major builder skill)
- Improved CLI with better help text and error handling
- Centralized logging and improved error handling
- Multiple practical examples in the `examples/` folder

### Changed
- Major improvements to first-run experience and startup messaging
- Significant documentation overhaul (README, Getting Started, CLI Reference)
- Better structure and consistency across the project

### Fixed
- Smoke test compatibility improvements
- More graceful handling when no skills are loaded

## [0.5.0] - Previous Development Versions

- Core ReAct loop and tool system
- Initial set of auditor skills (security, build hygiene, schema, etc.)
- Basic CLI (`run`, `skills`)
- Initial documentation
