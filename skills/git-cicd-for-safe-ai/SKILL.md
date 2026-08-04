---
name: git-cicd-for-safe-ai
description: Use when designing, reviewing, or hardening Git workflows, CI/CD pipelines, branch protection, and release processes for AI systems and agentic codebases. Handles safe defaults, HITL on production paths, secret hygiene, evaluation gates, and sovereignty-aware delivery. Trigger phrases include safe CI, AI CI/CD, branch protection for agents, release safety, git for AI, pipeline hardening.
metadata:
  version: "0.1.0"
  status: design-target
  owner: Coastal Alpine Tech
  last_updated: "2026-07-28"
  tier: delivery
  hitl_level: L2 on production and main
  cultural_sensitivity: low-medium
---

# Git & CI/CD for Safe AI

## Purpose

Establish reliable, auditable, and human-controlled delivery practices for AI agents, skills, and edge systems. This skill prevents common failure modes (force-pushes to main, unreviewed agent changes, secret leakage, untested model behaviour reaching production) while remaining practical for a small team.

## When to Use

- Setting up or reviewing repositories that contain agent code, skills, or model-serving logic.
- Designing branch protection, required checks, and release gates.
- Hardening CI for AI-specific risks (prompt injection in tests, non-deterministic behaviour, large model artefacts).
- Preparing evidence of delivery maturity for grants, partners, or diligence.
- Recovering from a bad merge or broken main branch.

## Core Principles

1. **Main is protected**  
   No direct pushes. All changes via pull request. Required status checks must pass.

2. **Humans own the merge**  
   Agents may open PRs and propose changes. Humans review and merge.

3. **Tests before trust**  
   Unit, integration, and behavioural/eval checks run automatically. Failures block merge.

4. **Secrets never in git**  
   Use environment secrets, `.gitignore`, and pre-commit hygiene. Scan for secrets in CI.

5. **Reproducible releases**  
   Versioned artefacts, changelog, and clear promotion path from design-target → higher maturity.

6. **Sovereignty-aware delivery**  
   Avoid pipelines that force data or model weights into uncontrolled foreign infrastructure without explicit decision.

## Minimum Safe Repository Setup

- Default branch protected (main or master).
- Require pull request before merging.
- Require at least one status check (CI) to pass.
- Block force pushes and deletions of the default branch.
- CODEOWNERS or explicit review for critical paths (skills/, security/, data/).
- Pre-commit or CI secret scanning.
- Clear `CHANGELOG` or release notes discipline.

## AI-Specific CI Considerations

- Separate deterministic tests from non-deterministic model behaviour tests.
- Treat evaluation harness results as first-class evidence (pass/fail thresholds).
- Pin model versions or container images where possible.
- Avoid running unbounded agent loops in CI without resource and time limits.
- Store large model artefacts outside the git history.

## HITL Gates

- Any change that modifies HITL logic, security controls, or data-sovereignty gates requires explicit human review.
- Production or customer-facing releases require founder (or designated) approval.
- Agents must not be granted write access to main or the ability to merge their own PRs.

## Relationship to Existing Skills

- Extends `build-ci-hygiene`, `release-preflight`, `branch-protection-rollout`, `ci-failure-parser`, `ci-failure-triage`.
- Supports `agent-hardening` and `aether-git-workflow`.
- Provides delivery evidence for grants and enterprise conversations.

## Anti-Patterns

- Allowing agents to push directly to main.
- “It works on my machine” releases without CI.
- Storing API keys or service-role secrets in the repository.
- Treating model evaluation as optional.
- Force-pushing to recover from mistakes instead of proper revert + post-mortem.

## Success Criteria

A team using this skill should be able to:

1. Configure a protected default branch with required checks.
2. Run automated tests and basic evaluation gates on every PR.
3. Prevent secret leakage through tooling and process.
4. Produce a clear, auditable path from change to production.
5. Demonstrate delivery maturity without over-claiming certification.

## Version & Status

- Version: 0.1.0
- Status: Design-target (L1)
- Next: Add concrete GitHub Actions templates and branch-protection scripts after first application.
