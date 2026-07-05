---
name: git-workflow
description: Handles safe git operations including creating branches, committing changes, pushing, and opening pull requests. Always respects approval gates on high-risk actions.
version: "0.1.0"
type: workflow
requires_hitl: true
cultural_sensitivity: low
tags: [git, workflow, branch, commit, push, pr]
---

# Git Workflow Manager

## Overview
This skill manages the full git lifecycle for code changes in a safe, auditable way. It is designed to be used by other skills (especially remediation skills) when they need to persist fixes.

## When to Use
- When a remediation or change needs to be committed to version control.
- When creating a feature branch for automated fixes.
- When pushing changes or opening a Pull Request after fixes have been applied.

## Instructions

### 1. Branch Creation
- Always create a new branch for changes using a clear naming convention (e.g. `fix/<short-description>` or `audit/<date>`).
- Never commit directly to `main` or `master`.

### 2. Committing Changes
- Generate a clear, conventional commit message.
- Include a short summary of what was fixed and why.

### 3. Pushing & Pull Requests
- Push the branch to the remote repository.
- Optionally open a Pull Request with a good description.
- Always include relevant context (e.g. linked issue or error details).

### 4. Safety & Approval
- **All git operations that modify the repository require human approval** before execution.
- Use the orchestrator’s approval system before running `git commit`, `git push`, or creating a PR.

## Guardrails & Constraints
- Never force push.
- Never commit directly to protected branches.
- Always require explicit human approval for `commit`, `push`, and PR creation.
- Log all git actions clearly.

## Input / Output

**Input**: Description of changes, files modified, and reason for the change.  
**Output**: Branch name, commit hash, and PR link (if created).

## Examples

**Example 1:**
Input: "Fixed error leaking in /api/users route"  
Output: Created branch `fix/error-leaking-users`, committed changes, opened PR #42.
