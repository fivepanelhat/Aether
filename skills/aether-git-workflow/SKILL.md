---
name: aether-git-workflow
description: Use when the user wants Aether to prepare, execute, or manage Git and GitHub operations for the Whānau Preterm Support Hub or related projects. Covers feature branching, conventional commits, Pull Request preparation, code review support, and safe maintenance workflows. Always enforces explicit user approval before any commit, push, or branch operation.

metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
---

# Aether Git Workflow

This skill enables Aether to handle all Git and GitHub interactions safely and professionally while maintaining full user control through strong HITL gates. It eliminates manual copy-paste of commands and ensures consistent, high-quality Git history and PRs.

## Core Rules

- Never commit, push, create branches, or open PRs without explicit user approval at each gate.
- Always work on short-lived feature branches (never directly on main unless for approved hotfixes).
- Use Conventional Commits format.
- Every Pull Request must include a clear description covering: what changed, why, how it was tested, accessibility impact, and any cultural or Te Tiriti considerations.
- Provide the user with either exact commands they can run, or execute them only after approval.
- Keep the Git history clean, reviewable, and meaningful for future contributors and cultural reviewers.

## Standard Workflow

When asked to implement a change:

1. Confirm the feature branch name (suggest a clear, conventional name).
2. Ensure the branch is up to date with main.
3. Make code changes only after plan approval (see aether-core).
4. After changes are complete and validated locally (lint, type-check, build, relevant tests), prepare the commit(s).
5. Present the exact `git diff` or summary of changes for review.
6. Draft the commit message(s) and ask for approval.
7. Once approved, either provide the precise commands or execute the commit after final confirmation.
8. Push the branch (after approval) and prepare the Pull Request.
9. Draft a high-quality PR title and description.
10. After merge (or during review), assist with any requested changes using the same gated process.

## Pull Request Description Template

Every PR description should include these sections (customise as needed):

```markdown
## Summary
One paragraph summary of the change.

## Motivation / Problem
What problem or opportunity does this address?

## Changes
- Bullet list of key changes

## Testing & Validation
- What was tested locally
- Accessibility / WCAG checks performed
- Any cultural safety considerations reviewed

## Te Tiriti & Cultural Alignment
(If relevant) How this change respects rangatiratanga, kaitiakitanga, or supports equitable outcomes for whānau.

## Screenshots / Evidence
(If UI change)

## Checklist
- [ ] Code follows project style and linting rules
- [ ] Accessibility verified (WCAG 2.2 AA where applicable)
- [ ] No PHI or sensitive data committed
- [ ] Documentation updated if needed
```

## Maintenance & Housekeeping Tasks

When asked to perform maintenance:
- Identify stale branches and propose cleanup (with approval).
- Help resolve merge conflicts by presenting clear options.
- Assist with release preparation, tagging, and changelog updates.
- Support reverting changes safely when needed.

## Communication

- Present Git-related actions as clear proposals with risks highlighted.
- Use tables or structured lists when showing multiple options or commands.
- Always state what will happen if the user approves vs what happens if they decline.
- Flag any situation where force-push, history rewrite, or sensitive file changes are involved — these require extra caution and explicit approval.
