---
name: aether-whanau-hub-architecture
description: Use this skill when working on the Whānau Preterm Support Hub NZ (Front_Line_Whanau / whanau-preterm-support-hub repositories). Provides deep, production-accurate knowledge of the current agentic architecture (Aether Summit orchestrator + specialist agent fleet), codebase structure, cultural safety patterns, i18n implementation, Supabase RLS + pgvector RAG, guardrails, HITL protocols, and Te Tiriti-aligned development practices extracted from the live GitHub codebase and ongoing chats. Load in addition to aether-core for any architecture, agent development, prompt refinement, or full-stack feature work on the Hub.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
---

# Aether Whānau Hub Architecture Skill

Deep, production-oriented knowledge of the Whānau Preterm Support Hub NZ architecture and practices.

## When to Load

- Any architecture, agent, prompt, or full-stack work on Front_Line_Whanau / Hub
- Designing specialist agents under Aether Summit for Hub domains
- Cultural safety, i18n, Supabase RLS, or pgvector RAG changes
- HITL and guardrail design for whānau-facing flows

## Core Architecture Themes

- Aether Summit orchestrator + specialist fleet
- Local-first and sovereignty-aware data paths
- Supabase RLS + pgvector RAG patterns
- Cultural safety and Te Tiriti-aligned development
- Medical and support disclaimers on relevant surfaces
- HITL for high-impact or cultural content

## Working Rules

- Load `aether-core` first
- Prefer existing Hub patterns over new invention
- Never invent iwi endorsement or clinical claims
- Keep health and cultural content behind appropriate gates and disclaimers

## Related Skills

- `aether-core`
- `hub-nextjs-component`
- `aether-ui-ux-platform`
- `aether-hitl-protocol`
- `aether-data-sovereignty`
- `te-mana-raraunga-controls`
