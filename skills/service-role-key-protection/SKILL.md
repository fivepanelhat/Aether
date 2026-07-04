---
name: service-role-key-protection
description: Ensures admin-level Supabase operations always use `createAdminClient()` instead of manually constructing the service role key.
version: "0.1.0"
type: security
requires_hitl: false
cultural_sensitivity: high
tags: [security, supabase, auth, admin]
---

# Service Role Key Protection

## Overview
Prevents insecure usage of the Supabase service role key by enforcing the use of a centralized `createAdminClient()` helper instead of manually importing and constructing the key in routes.

## When to Use
- When reviewing or writing any route that requires admin-level database access.
- During security audits.
- When refactoring routes that currently use `SUPABASE_SERVICE_ROLE_KEY` directly.

## Instructions

### 1. Identify Unsafe Usage
Look for patterns like:
```ts
import { createClient } from '@supabase/supabase-js';
const supabase = createClient(url, process.env.SUPABASE_SERVICE_ROLE_KEY);
```

### 2. Apply the Helper
Replace manual creation with the centralized `createAdminClient()` helper.

```ts
import { createAdminClient } from '@/lib/supabase/admin';
const supabase = createAdminClient();
```
