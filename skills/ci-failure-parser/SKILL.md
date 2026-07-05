---
name: ci-failure-parser
description: Parses and extracts useful information from CI failures, GitHub Actions logs, test errors, and GitHub issue/PR comments. Helps turn raw failure data into structured, actionable information.
version: "0.1.0"
type: workflow
requires_hitl: false
cultural_sensitivity: low
tags: [ci, github, parsing, errors, logs]
---

# CI / GitHub Failure Parser

## Overview
This skill takes raw CI output, GitHub Actions logs, or error messages and extracts the key information needed for debugging (failing tests, stack traces, relevant files, error type, etc.).

## When to Use
- When a CI pipeline fails.
- When a GitHub Action reports an error.
- When processing error notifications from GitHub Issues or Pull Requests.

## Instructions

### 1. Parse Input
- Accept raw log output, GitHub webhook payload, or error text.
- Identify the type of failure (test failure, lint error, build error, deployment failure, etc.).

### 2. Extract Key Information
- Failing test name(s)
- Stack trace / error message
- Relevant file paths and line numbers
- Command that failed
- Environment/context (Node version, OS, etc.)

### 3. Structure the Output
- Return a clean, structured summary that other skills (especially `error-remediation-orchestrator`) can use.

## Guardrails & Constraints
- Focus on extracting factual information rather than guessing the root cause.
- Be careful with very large log outputs — summarize when appropriate.

## Input / Output

**Input**: Raw CI log, GitHub Actions failure, or error text.  
**Output**: Structured failure report (failing tests, error messages, file locations).
