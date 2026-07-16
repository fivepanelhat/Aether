---
name: notification-responder
description: Generates clear, professional responses for GitHub comments, email, or other channels during remediation workflows. Used to request approval or provide status updates.
version: "0.1.0"
type: workflow
requires_hitl: false
cultural_sensitivity: low
tags: [notification, github, communication, response]
---

# Notification Responder

## Overview
Helps Aether communicate clearly with humans during automated workflows (especially remediation).

## When to Use
- When requesting human approval for a proposed fix.
- When providing status updates on a remediation task.
- When replying to GitHub issues or PRs.

## Instructions

### 1. Understand Context
- Know what stage the task is at (analysis complete, fix proposed, changes applied, etc.).
- Know what action is needed from the user.

### 2. Craft Response
- Be clear, concise, and professional.
- Include what was found and what action is being requested.
- Provide enough context for the user to make a quick decision.

### 3. Include Next Steps
- Clearly state what you need from the user (e.g., approval to apply the fix).

## Guardrails & Constraints
- Never overpromise on timelines or outcomes.
- Be transparent when human input is required.

## Input / Output

**Input**: Current task status and what needs to be communicated. 
**Output**: Well-written message ready to post or send.
