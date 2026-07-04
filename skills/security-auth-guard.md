---
name: security-auth-guard
description: Adds authentication and role-based access guards to sensitive API routes following established patterns.
version: "0.1.0"
type: security
requires_hitl: false
cultural_sensitivity: medium
---

# Security & Auth Guard Pattern

## Overview
Standardises the addition of `requireAuth` + role checks on routes that use service-role keys or handle sensitive data.

## When to Use
- Protecting routes that use `service_role` Supabase client
- Adding role checks (`admin`, `practitioner`, etc.)
- Narrowing `.select()` queries and adding `.limit()`
- Adding rate limiting to sensitive endpoints

## Instructions
1. Identify routes using service-role keys without auth.
2. Import and apply the existing `requireAuth` pattern.
3. Add role validation where appropriate.
4. Narrow database queries and add limits.
5. Add rate limiting using the established Upstash pattern.

## Guardrails & Constraints
- Never expose service-role keys without auth + role checks.
- Prefer narrow column selection over `.select('*')`.
- Always apply rate limiting on mutating or expensive endpoints.
