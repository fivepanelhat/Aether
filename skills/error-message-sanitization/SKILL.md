---
name: error-message-sanitization
description: Prevents leaking internal error details (error.message, stack traces) to API clients. Ensures only safe, user-friendly messages are returned.
version: "0.1.0"
type: security
requires_hitl: false
cultural_sensitivity: low
tags: [security, error-handling, sanitization, api]
---

# Error Message Sanitization Guard

## Overview
Enforces a strict rule: **never expose raw error messages or stack traces to API clients**. All errors should be sanitized before being returned in responses.

## When to Use
- When building or reviewing any API route that catches errors.
- During security hardening.
- When fixing routes that currently leak `error.message` to the frontend.

## Instructions

### 1. Identify Error Leaks
Search for patterns such as:
```ts
return NextResponse.json({ error: error.message })
console.error(error)
```

### 2. Apply Sanitization
Always replace raw errors with generic, safe responses for the client, while logging the raw error internally for debugging.

```ts
// Bad
return NextResponse.json({ error: error.message }, { status: 500 });

// Good
console.error("Internal error:", error);
return NextResponse.json(
  { error: "An unexpected error occurred. Please try again later." },
  { status: 500 }
);
```
