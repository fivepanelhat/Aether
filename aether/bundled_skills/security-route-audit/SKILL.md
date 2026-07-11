---
name: security-route-audit
description: Systematically audits API routes for common security vulnerabilities including auth bypass, injection, input validation, and error leaking.
version: "0.1.0"
type: security
requires_hitl: false
cultural_sensitivity: medium
tags: [security, audit, routes, validation, auth]
---

# Security Route Audit Pattern

## Overview
Provides a structured approach to auditing all API routes in a Next.js + Supabase application for security issues. Covers authentication, authorization, input validation, error handling, and data exposure risks.

## When to Use
- Before major releases or security reviews.
- When adding new API routes or modifying existing ones.
- During regular security hardening sprints.
- When investigating potential data leaks or unauthorized access.

## Instructions

### 1. Inventory All Routes
- List every file under `app/api/` (or `pages/api/`).
- Group routes by sensitivity (public, authenticated, admin-only).

### 2. Check for Common Vulnerabilities
For each route, verify the following:

- **Authentication**: Does the route properly verify the user via `getUser()` or middleware?
- **Authorization / Role Checks**: Are role checks (`admin`, `practitioner`, etc.) enforced on sensitive operations?
- **Input Validation**: Are Zod schemas used? Are they strict (`z.string()`, `z.number()`) or loose (`z.any()`)?
- **Error Handling**: Are raw `error.message` or stack traces ever sent to the client?
- **Service Role Key Usage**: Is `createAdminClient()` used instead of constructing the key manually?
- **Data Exposure**: Does the route return unapproved or sensitive data to unauthenticated users?
- **Injection Risks**: Are CSV exports, LLM prompts, or database queries properly sanitized?

### 3. Prioritize by Severity
- **CRITICAL**: Error leaking, raw service role key usage, missing auth on sensitive routes.
- **HIGH**: Missing validation, CSV injection, weak schemas, unauthorized data access.
- **MEDIUM**: CSP issues, missing env schema entries, weak input sanitization.

### 4. Auto-Remediation Workflow
- **Branch**: Create a new git branch `audit/<date>-<topic>`.
- **Patch**: Apply fixes systematically (batch similar issues together).
- **Verify**: Re-run the test suite, type-check, and lint after patching.
- **Report**: Output a summary of the diffs and test results as raw output for the user to review.

## Guardrails & Constraints
- Never expose internal error details to clients.
- Always use `createAdminClient()` for admin-level operations.
- Treat any route that touches user data or funding as high sensitivity.
- Document all changes for auditability.

## Input / Output

**Input**: A request to perform a security audit on the current API surface.  
**Output**: A prioritized list of findings with recommended fixes and patched code where applicable.

## Examples

**Before**: Multiple routes leaking `error.message`, using raw service role keys, and returning unapproved stories to anonymous users.

**After**: All routes properly validated, errors sanitized, role checks enforced, and sensitive data protected.

## References
- Previous security audit sessions in the project
- OWASP Top 10 for API security
- Supabase security best practices
