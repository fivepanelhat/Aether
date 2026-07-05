# Changelog

All notable changes to Aether will be documented in this file.

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
- `aether validate` command for installation checks
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
