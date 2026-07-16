# Skill Development Guide

This guide explains how to create high-quality, effective skills for Aether.

## What Makes a Good Skill?

A good skill should be:

- **Focused** - It solves one clear problem or workflow well.
- **Reusable** - It can be used across many different situations.
- **Clear** - The instructions are easy to understand and follow.
- **Safe** - It respects human approval gates on high-risk actions.
- **Extensible** - It can be improved over time without major rewrites.

## Skill Structure

Every skill must follow this basic structure:

### Required Frontmatter

```yaml
---
name: your-skill-name
description: Clear description of what the skill does and when it should be used.
version: "0.1.0"
type: workflow | component | security | orchestration | hygiene
requires_hitl: true | false
cultural_sensitivity: low | medium | high
tags: [tag1, tag2]
---
```

## Instructions

1. First, analyze the goal and identify relevant files.
2. Use the `codebase_search` tool to locate potential issues.
3. Review each suspicious file carefully.

## Guardrails

Never commit directly to the `main` branch. 
This prevents accidental changes to production code and maintains a clean git history.
