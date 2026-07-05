# Aether CLI Reference

This document describes all available commands for the Aether command-line interface.

## Installation

```bash
pip install -e .
aether --help
```

## `run`

Execute a task with the orchestrator.

```bash
aether run <goal> [options]
```

### Arguments

| Argument | Description | Required |
|----------|-------------|----------|
| `goal` | The task or objective to work on | Yes |

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-steps` | Maximum number of steps in the ReAct loop | 8 |
| `--memory` | Path to a file for persisting memory across runs | None |

### Examples

```bash
# Basic usage
aether run "Audit all API routes for security issues"

# Run with more steps
aether run "Improve agent context handling and reliability" --max-steps 10

# Use persistent memory
aether run "What did we decide about authentication last time?" --memory aether_memory.json
```

## `skills`

List all skills currently available to Aether.

```bash
aether skills
```

### Example Output

```text
AVAILABLE SKILLS

security-auth-guard
  Type: security | Requires Approval: No
  Adds authentication and role-based access guards to sensitive API routes

agent-reliability-context
  Type: orchestration | Requires Approval: No
  Improves agent behavior around conversation history and context retention

build-ci-hygiene
  Type: hygiene | Requires Approval: No
  Prevents module-level environment crashes and ensures reliable CI builds

...
```

## Planned / Future Commands

These commands are not yet implemented but are planned for future versions of Aether.

### `init`
Initialize Aether in the current project (creates config, memory file, etc.).

```bash
aether init
```
*Status: Planned*

### `validate`
Validate the current project against selected skills (e.g. security, accessibility, design system).

```bash
aether validate --skills security,design
```
*Status: Planned*

### `list`
List files, skills, or previous tasks.

```bash
aether list tasks
aether list skills
```
*Status: Planned*

### `export`
Export task history or results to a file.

```bash
aether export --output report.md
```
*Status: Planned*

### `config`
View or edit Aether configuration.

```bash
aether config show
aether config set memory_path ./memory.json
```
*Status: Planned*

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--help` | Show help message | - |
| `--version` | Show Aether version (planned) | - |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | User cancelled / rejected action |

*Note: This document will be updated as new commands are added.*
