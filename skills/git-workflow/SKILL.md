---
name: git-workflow
description: Manages safe git operations including branch creation, committing changes, pushing, and opening pull requests. Always requires human approval for destructive or high-impact git actions.
version: "0.2.0"
type: workflow
requires_hitl: true
cultural_sensitivity: low
tags: [git, branch, commit, push, pr, workflow]
---

# Git Workflow Manager

## Overview
This skill provides controlled git operations so other skills (especially remediation skills) can persist code changes safely and consistently.

## When to Use
- When code changes need to be committed to version control.
- When creating a feature/fix branch for automated changes.
- When pushing changes or opening a Pull Request.

## Instructions

### Branch Creation
- Always create a new branch using a clear convention: `fix/<description>` or `audit/<date>`.
- Never work directly on `main` or `master`.

### Committing Changes
- Generate a clear, conventional commit message.
- Include a short summary of the problem and the fix.

### Pushing & Pull Requests
- Push the branch to the remote.
- Optionally open a Pull Request with a good description and link to the original issue/error.

### Approval Requirements
- Creating branches is generally low-risk.
- **Committing, pushing, and opening PRs require explicit human approval** before execution.

## Guardrails & Constraints
- Never force push.
- Never commit directly to protected branches.
- All modifying git operations must go through the orchestrator's approval system.
- Log every git action taken.

## Input / Output

**Input**: Summary of changes and reason for the commit. 
**Output**: Branch name, commit hash, and Pull Request URL (if created).
