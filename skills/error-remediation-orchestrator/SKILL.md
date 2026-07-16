---
name: error-remediation-orchestrator
description: Orchestrates the full remediation process - receives an error, analyzes it using other skills, proposes fixes, applies changes (with approval), and uses git-workflow to persist the fix.
version: "0.2.0"
type: orchestration
requires_hitl: true
cultural_sensitivity: low
tags: [error, debugging, remediation, fix, orchestration]
---

# Error Remediation Orchestrator

## Overview
This is the central coordinator for turning errors (from CI, GitHub, tests, etc.) into resolved code changes. It intelligently uses other skills during the process.

## When to Use
- When a CI failure, test error, or GitHub issue is reported.
- When you want to automatically investigate and propose a fix for a failure.

## Instructions

### 1. Receive Error
- Accept error details (CI log, stack trace, GitHub issue, failing test, etc.).
- Use `ci-failure-parser` if the input is raw CI output.

### 2. Analyze Root Cause
- Use relevant auditor skills (e.g. `security-route-audit`, `build-ci-hygiene`) to investigate.
- Identify the files and code responsible for the failure.

### 3. Propose Fix
- Generate the necessary code changes.
- Clearly explain the reasoning behind the proposed solution.

### 4. Apply Changes (with Approval)
- Use `file_writer` to apply fixes.
- Run relevant tests or linting to validate the fix.

### 5. Persist Changes
- Use `git-workflow` to create a branch, commit, and push (with approval).

## Guardrails & Constraints
- **Human approval is required** before applying code changes and before any git commit/push.
- Always validate fixes before committing.
- Be transparent about what was changed and why.

## Input / Output

**Input**: Error information (CI failure, stack trace, GitHub issue, etc.). 
**Output**: Proposed fix + branch/PR containing the resolution.
