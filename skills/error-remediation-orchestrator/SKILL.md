---
name: error-remediation-orchestrator
description: Coordinates the full process of receiving an error, analyzing it, proposing fixes, applying changes, and using git-workflow to commit the results. Acts as the central coordinator for automated debugging and patching.
version: "0.1.0"
type: orchestration
requires_hitl: true
cultural_sensitivity: low
tags: [error, debugging, remediation, fix, orchestration]
---

# Error Remediation Orchestrator

## Overview
This skill orchestrates the end-to-end process of turning an error (from CI, GitHub, email, etc.) into a resolved code change. It coordinates analysis, fix generation, validation, and git operations.

## When to Use
- When an error or failure is reported (via GitHub, CI, email, or manual trigger).
- When you want to automatically debug and propose a fix for a failing test or error.

## Instructions

### 1. Receive & Parse Error
- Accept error details (stack trace, failing test, CI log, GitHub issue, etc.).
- Use supporting skills (e.g. `ci-failure-parser`) to extract relevant information.

### 2. Analyze the Problem
- Use relevant auditor skills (`security-route-audit`, `build-ci-hygiene`, etc.) to investigate the root cause.
- Identify the files and code responsible for the error.

### 3. Propose Fixes
- Generate the code changes needed to resolve the issue.
- Explain the reasoning behind the proposed fix.

### 4. Apply & Validate
- Use the `file_writer` tool to apply changes (with approval).
- Run relevant tests or linting to validate the fix.

### 5. Persist Changes
- Use the `git-workflow` skill to create a branch, commit, and push the fix (with approval).

## Guardrails & Constraints
- **Every major step requires human approval** before proceeding (especially applying code changes and git operations).
- Do not blindly apply fixes without validation.
- Always provide a clear explanation of the proposed fix to the user.

## Input / Output

**Input**: Error details (stack trace, CI failure, GitHub issue, etc.).  
**Output**: Proposed fix + branch/PR with the resolution.
