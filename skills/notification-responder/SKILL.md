---
name: notification-responder
description: Generates appropriate responses to notifications received via GitHub, email, Slack, or other channels. Used to communicate status updates, proposed fixes, or requests for approval.
version: "0.1.0"
type: workflow
requires_hitl: false
cultural_sensitivity: low
tags: [notification, communication, github, email, response]
---

# Notification Responder

## Overview
This skill helps generate clear, professional responses when Aether needs to communicate with humans (via GitHub comments, email, Slack, etc.). It is especially useful during remediation workflows.

## When to Use
- When reporting analysis results or proposed fixes.
- When requesting human approval for a change.
- When providing status updates on remediation tasks.

## Instructions

### 1. Determine Context
- Understand what triggered the notification (CI failure, GitHub issue, email, etc.).
- Know what stage the remediation is at (analysis done, fix proposed, changes applied, etc.).

### 2. Generate Appropriate Response
- Be clear and concise.
- Include relevant details (what was found, what fix is proposed, what action is needed from the user).
- Use a professional but friendly tone.

### 3. Include Next Steps
- Clearly state what you need from the user (approval, more information, etc.).
- Provide context so the user can make a quick decision.

## Guardrails & Constraints
- Never make promises about timelines or outcomes that cannot be guaranteed.
- Be transparent when Aether is unsure or needs human input.

## Input / Output

**Input**: Current status of a task and what needs to be communicated.  
**Output**: Well-structured message ready to be sent via GitHub, email, or Slack.
