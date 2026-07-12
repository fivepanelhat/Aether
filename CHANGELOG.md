# Changelog


## Hybrid platform update (July 2026)

- Dual-platform installers: `install.sh` (Linux/macOS) and `install.ps1` (Windows)
- Mermaid system maps updated for hybridisation (Core · Weaver · Aether · stack) and Windows + Linux hosts
- Architecture overview images refreshed for hybrid stack + dual OS targets
- Developer setup / installation docs cover Windows and Linux prerequisites and packages

All notable changes to Aether will be documented in this file.

## [0.7.0] - 2026-07

### Added — Edge AI + Computer Use (hybrid)
- **`aether computer`**: operate a real desktop on **Windows and Linux** (and macOS).
  - `computer run "<goal>"` — agentic screenshot→decide→act loop driven by a **local**
    Ollama vision model (`qwen2.5-vl` class). Fully on-device; nothing is exfiltrated.
  - Direct, model-free control: `shot`, `info`, `click`, `move`, `type`, `key`, `scroll`.
- **`aether doctor`** — readiness check for display/backend + local Ollama + models.
- New `aether.computer` package: cross-platform PyAutoGUI backend with coordinate
  clamping, fail-safe, and a `AETHER_COMPUTER_DRY_RUN` rehearsal switch; Aether tools
  (`screenshot`, `computer_*`, `shell_exec`) registered into the ReAct orchestrator.
- Actuating tools are gated by the existing **guardrails / HITL** layer; goals are
  screened for prompt injection before any action runs. Read-only capture is ungated.
- `OllamaClient.chat()` accepts `images=` for multimodal (vision) prompts.
- Optional extras `pip install "aether[computer]"` (pyautogui, Pillow) and `[all]`.
- Cross-platform downloadable installers: `install.sh` (Linux/macOS) and `install.ps1`
  (Windows) — venv, PATH launcher, skills, and Ollama check in one command.
- Tests: `tests/test_computer_use.py` (backend clamping/dry-run, tool gating, agent loop,
  approval-deny halt, injection block).

## [0.6.8] - 2026-07

### Fixed
- Webhook module imports without FastAPI/tenacity (optional extras); CI no longer fails on `ModuleNotFoundError: fastapi`.
- CI installs `.[dev,webhook]`; CLI smoke falls back to `python -m aether.cli`.

## [0.6.7] - 2026-07

### Changed (cross-platform)
- Path sandbox uses `commonpath` + Windows `normcase` (mixed `/`\\`, case-insensitive drives).
- `escape_for_shell` uses `subprocess.list2cmdline` on Windows and `shlex.quote` on POSIX.
- Logging/CLI force UTF-8 stdio where supported; log files open with `encoding=utf-8`.
- Skill loader accepts `SKILL.md` or `skill.md` (Linux case-sensitive trees).
- CI matrix: **ubuntu-latest** and **windows-latest** × Python 3.10 / 3.12; portable CLI smoke.

## [0.6.6] - 2026-07

### Added
- **Packaged skills**: `aether/bundled_skills` ships with the wheel; discovery falls back to package data after CWD / `~/.aether/skills`.
- **`aether init`**: copies bundled skills to `~/.aether/skills` and `./skills` (`--force`, `--user-only`, `--project-only`).
- Shared `aether.paths` helpers for skills resolution and path sandboxing.

### Security
- **`codebase_search`** and **`directory_lister`** respect the same `allowed_root` sandbox as file read/write (blocks path traversal).

## [0.6.5] - 2026-07

### Security
- **Skill HITL enforced**: skills with `requires_hitl: true` or `cultural_sensitivity: high` require approval (same path as `file_writer`).
- **Webhook propose-only by default**: CI remediation no longer sets `auto_remediate=True`. Opt in with `AETHER_WEBHOOK_AUTO_REMEDIATE=1`.

### Added
- `TaskState.skill_execution_results` and `active_skill_instructions` for audit + CLI.
- Skill application injects a binding playbook block into task state (visible in `summarize()` / ReAct CURRENT STATE).

### Changed
- `_execute_skill` records structured application metadata (version, HITL, cultural sensitivity).
- Webhook CLI banner documents propose-only vs auto-remediate env flag.

## [0.6.4] - 2026-07

### Added (skills)
- **`kiwi-edge-architecture`** — Kiwi Edge system map (field → fabric → Core → Weaver → portals → Ollama/Hailo → trust).
- **`security-notifications-triage`** — Dependabot / GHSA / CodeQL / audit response playbook.
- **`te-mana-raraunga-sovereignty`** — Te Mana Raraunga 2018 data-sovereignty constraints.
- Full **Skills Catalog** refresh (`docs/SKILLS_CATALOG.md`) + README Skills section.

### Changed
- `build-ci-hygiene` → v0.2.0 (least-privilege Actions permissions + Dependabot).

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
