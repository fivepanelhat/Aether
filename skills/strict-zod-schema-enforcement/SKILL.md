---
name: strict-zod-schema-enforcement
description: Replaces loose validation schemas (z.any(), missing schemas) with strict, well-typed Zod schemas for all API inputs.
version: "0.1.0"
type: security
requires_hitl: false
cultural_sensitivity: low
tags: [security, validation, zod, schema, api]
---

# Strict Zod Schema Enforcement

## Overview
Enforces the use of strict, well-defined Zod validation schemas for all API route inputs instead of loose or missing validation (`z.any()`, no schema at all).

## When to Use
- When creating or modifying API routes that accept request bodies or query parameters.
- During security hardening and code reviews.
- When fixing routes that currently use weak or missing validation.

## Instructions

### 1. Identify Weak Validation
Look for:
- `z.any()` in schemas
- Routes with no Zod schema at all
- Overly permissive schemas (e.g. accepting any object)

### 2. Define Strict Schemas
Example transformation:

```ts
// Weak
const AgentQuerySchema = z.object({
 history: z.any()
});

// Strong
const MessageSchema = z.object({
 role: z.enum(["user", "assistant"]),
 content: z.string().min(1).max(4000)
});

const AgentQuerySchema = z.object({
 history: z.array(MessageSchema),
 // ... other fields
});
```
