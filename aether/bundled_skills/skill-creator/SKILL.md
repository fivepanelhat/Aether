---
name: skill-creator
description: Helps create, test, evaluate, and iteratively improve new Aether skills. Use this skill whenever the user wants to build a new reusable capability, turn a workflow into a skill, or significantly improve an existing skill through testing and feedback.
version: "0.1.0"
type: orchestration
requires_hitl: false
cultural_sensitivity: low
tags: [skill, creation, iteration, evaluation, meta]
---

# Skill Creator

## Overview
This skill guides the creation and iterative improvement of high-quality Aether skills. It follows a structured loop of drafting, testing, evaluating with the user, and refining until the skill is reliable and useful.

## When to Use
- The user wants to turn a workflow, pattern, or process into a reusable skill.
- The user has an idea for a new capability and wants help structuring it properly.
- An existing skill needs significant improvement based on real usage or feedback.
- The user wants to systematically test and evaluate a skill before relying on it.

## Instructions

### 1. Capture Intent
Start by understanding what the user wants the skill to achieve.

Ask clarifying questions if needed:
- What should this skill enable someone to do?
- When should this skill trigger? (What kinds of user requests or contexts?)
- What should the output look like?
- Does this skill have objectively verifiable outputs (e.g. code, files, structured data) or is it more subjective (e.g. writing style, advice)?

Extract any existing workflow from the conversation history first before asking new questions.

### 2. Interview and Research
Before writing anything, gather context:
- Edge cases and failure modes
- Input/output formats
- Example files or previous attempts
- Success criteria
- Any dependencies or tools the skill should use

Do light research if needed (e.g. look at similar existing skills or documentation).

### 3. Write the Skill
Create a new skill following the official Aether `SKILL.md` format:

- Use clear, imperative instructions
- Include a strong `description` in the frontmatter (make it reasonably "pushy" so the skill actually gets used when relevant)
- Follow progressive disclosure (keep the main `SKILL.md` focused)
- Add examples where helpful
- Explain the *why* behind important instructions rather than just using heavy "MUST" language

Save the skill in `skills/<skill-name>/SKILL.md`.

### 4. Create Test Cases
After drafting the skill, propose 2–4 realistic test prompts that a real user might give.

Ask the user:
- "Here are a few test cases I'd like to try. Do these look right, or would you like to add/change any?"

Save test cases in a workspace directory for the iteration (e.g. `skill-workspace/iteration-1/`).

### 5. Test and Evaluate
Run the test cases both **with** the new skill and **without** it (baseline).

For each test case:
- Capture the outputs
- Compare the quality
- Discuss results with the user (qualitative feedback is usually most valuable)

If quantitative checks make sense (e.g. "does it produce valid JSON?", "does the file get created?"), define simple assertions.

### 6. Iterate
Based on user feedback and observed issues:
- Improve the skill
- Rerun the test cases in a new iteration folder (`iteration-2/`, etc.)
- Show the user the differences
- Repeat until the user is satisfied or feedback becomes consistently positive/empty

Focus improvements on:
- Generalization (avoid overfitting to the test cases)
- Removing unnecessary instructions
- Explaining the reasoning behind important steps
- Bundling repetitive helper logic into `scripts/` when it appears across multiple test cases

### 7. (Optional) Optimize Skill Triggering
Once the skill is working well, offer to improve the `description` field in the frontmatter for better automatic triggering. This involves creating trigger evaluation queries and running an optimization process.

## Guardrails & Constraints
- Never create skills that could be used for malicious purposes (malware, unauthorized access, data exfiltration, scams, etc.).
- Skills must be transparent in their intent. Do not create misleading or deceptive skills.
- Respect the user's preference on evaluation rigor. Some users prefer quick iteration over formal benchmarks.
- Always explain what you're doing and why, especially when the user is less technical.

## Input / Output

**Input**: A request to create or improve a skill, often with some description of what it should do.  
**Output**: A well-structured, tested `SKILL.md` file (and supporting files if needed) that is ready to be used.

## Communication Style
- Adapt your language to the user's technical comfort level.
- Explain terms like "evaluation", "assertion", or "baseline" if the user doesn't seem familiar with them.
- Be collaborative rather than overly prescriptive.

## References
- Official Aether Skill Format (`docs/AETHER_SKILL_FORMAT.md`)
- Existing high-quality skills in the `skills/` directory for reference
