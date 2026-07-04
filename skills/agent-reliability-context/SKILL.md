---
name: agent-reliability-context
description: Ensures agents maintain conversation history, use real tools, and have properly tuned guardrails.
version: "0.1.0"
type: orchestration
requires_hitl: false
cultural_sensitivity: high
---

# Agent Reliability & Context Management

## Overview
Addresses common failures in multi-agent systems: dropped history, poor tool use, overly aggressive guardrails, and streaming issues.

## When to Use
- Agents are giving incomplete or context-less answers
- Follow-up questions fail
- Agents deflect useful requests due to guardrails
- Streaming produces duplicated or broken output

## Instructions
1. Ensure full conversation history is passed to every agent and the classifier.
2. Equip agents with real tools (especially web search + citations) instead of relying on model memory.
3. Review and tune guardrails — remove blanket blocks that kill legitimate answers.
4. Fix streaming final events so the UI receives clean output.
5. Add consistent locale support across all agents.

## Guardrails & Constraints
- Guardrails must protect without blocking useful functionality.
- History must be preserved for multi-turn conversations.
- Agents that need external information should use tools, not model knowledge.
