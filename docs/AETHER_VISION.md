# Aether: Problems We’re Solving & How We’re Solving Them

## The 5 W’s

| Question | Answer |
|---------|--------|
| **Why** | Founders and small teams building important digital platforms (especially community and whānau-focused ones) are overwhelmed by repetitive technical work, context switching, and inconsistent quality. |
| **What** | Aether is a sovereign, culturally grounded agentic development orchestrator that helps users plan, build, and maintain high-quality software with strong human oversight. |
| **Who** | Primarily founders and small teams working on projects like the Whānau Preterm Support Hub NZ — people who need to move fast without sacrificing quality, accessibility, or cultural safety. |
| **Where** | Designed to work locally or in sovereign environments. Initially focused on the Whānau Preterm Support Hub, with the goal of being portable to other projects. |
| **When** | Right now — during active development of the Hub and similar platforms where reducing founder load and maintaining control is critical. |

---

## The Problems We’re Solving

### 1. High Cognitive Load & Context Switching
Founders constantly switch between planning, coding, reviewing, Git operations, and stakeholder communication. This leads to fatigue and slower progress.

### 2. Repetitive Technical Work
Many tasks (setting up components, adding auth guards, fixing build issues, writing migrations, etc.) are repetitive and could be accelerated with intelligent assistance.

### 3. Inconsistent Quality
AI-generated code and plans often lack consistency in accessibility, security, cultural considerations, and long-term maintainability.

### 4. Weak Guardrails & Oversight
Many AI coding tools offer little control. Important decisions (especially those affecting data, culture, or funding) are made without proper human review.

### 5. Lack of Cultural & Data Sovereignty
Most existing tools are not designed with Te Mana Raraunga or indigenous data sovereignty in mind. This creates misalignment when building platforms for Māori and Pacific communities.

### 6. Poor Long-term Learning
Most AI interactions start from zero every time. There is little compounding intelligence tailored to a specific project or set of values.

---

## How We’re Solving These Problems

| Problem | How Aether Addresses It |
|--------|--------------------------|
| **High cognitive load** | The orchestrator handles planning, tool use, and repetitive tasks so the user can stay at a higher level. |
| **Repetitive work** | Reusable skills + tool calling reduce the need to do the same work repeatedly. |
| **Inconsistent quality** | Skills encode standards (e.g. accessibility, cultural safety, security patterns) so outputs follow consistent practices. |
| **Weak oversight** | Strong Human-in-the-Loop (HITL) model with clear approval gates on high-impact actions. |
| **Lack of sovereignty** | Designed to run locally/self-hosted. Guardrails and skills can embed Te Mana Raraunga principles. |
| **No compounding learning** | Memory system + skill creation allows Aether to improve over time based on real work. |

---

## Core Approach

- **Stay Lightweight**: We are building a custom Python orchestrator first (instead of jumping straight to LangGraph) to maintain full control and sovereignty.
- **Skills over Prompts**: We use structured, versioned, reviewable skills instead of one-off prompts.
- **Tools + ReAct**: The orchestrator can reason and use tools (search codebase, read files, query memory, write files) in a controlled way.
- **Guardrails First**: Cultural sensitivity, HITL requirements, and security considerations are built into the system from the start.
- **Pragmatic Autonomy**: We are increasing autonomy step by step while keeping humans in control of important decisions.

---

## Guiding Principles

- User sovereignty first
- Search before building
- Completeness over shortcuts
- Principled self-improvement with care
- Te Mana Raraunga as a core constraint

---

**This document will evolve** as Aether develops and we learn what works best in practice.

Last updated: July 2026
