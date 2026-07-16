---
name: ci-failure-parser
description: Parses CI logs, GitHub Actions failures, and test errors into structured, actionable information that can be used by remediation skills.
version: "0.1.0"
type: workflow
requires_hitl: false
cultural_sensitivity: low
tags: [ci, github, parsing, errors, logs]
---

# CI / GitHub Failure Parser

## Overview
Converts noisy CI output and error logs into clean, structured data that other skills can reliably use.

## When to Use
- When processing CI failures or GitHub Actions errors.
- When an error notification contains raw logs or stack traces.

## Instructions

### 1. Parse Input
- Accept raw logs, GitHub webhook data, or error text.
- Identify failure type (test failure, build error, lint error, deployment failure, etc.).

### 2. Extract Key Details
- Failing test or command
- Error message / stack trace
- Relevant file paths and line numbers
- Environment information (if available)

### 3. Return Structured Output
- Provide a clean summary that `error-remediation-orchestrator` and other skills can consume.

## Guardrails & Constraints
- Focus on factual extraction rather than diagnosis.
- Handle large logs gracefully by summarizing when needed.

## Input / Output

**Input**: Raw CI log or error output. 
**Output**: Structured failure report.
