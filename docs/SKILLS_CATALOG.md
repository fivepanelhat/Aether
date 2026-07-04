# Aether Skills Catalog

This document lists all current skills available in Aether, along with when to use them.

## High-Value Skills

### security-auth-guard
**Type**: Security  
**Priority**: Very High  
**Description**: Adds authentication and role-based access guards to sensitive API routes.  
**Use When**: Auditing or hardening API security, especially routes using service role keys.

### agent-reliability-context
**Type**: Orchestration  
**Priority**: Very High  
**Description**: Improves agent behavior around conversation history, context retention, and guardrail tuning.  
**Use When**: Working with multi-turn agents or fixing unreliable agent responses.

### build-ci-hygiene
**Type**: Hygiene  
**Priority**: High  
**Description**: Prevents module-level environment crashes and ensures reliable CI builds.  
**Use When**: Fixing build failures or improving CI pipelines.

### schema-migration-hygiene
**Type**: Hygiene  
**Priority**: High  
**Description**: Detects schema drift and recommends safe database migrations and indexes.  
**Use When**: Adding new database features or fixing missing columns/indexes.

### design-system-unification
**Type**: Component  
**Priority**: High  
**Description**: Helps unify inconsistent design tokens, theming, and component styling across an application.  
**Use When**: Fixing visual inconsistencies or establishing design standards.

### release-engineering
**Type**: Workflow  
**Priority**: High  
**Description**: Standardizes versioning, building, testing, tagging, and releasing software.  
**Use When**: Preparing releases or setting up release processes.

### security-route-audit
**Type**: Security  
**Priority**: Very High  
**Description**: Provides a structured process for auditing API routes for security issues.  
**Use When**: Performing security reviews or hardening sprints.

### error-message-sanitization
**Type**: Security  
**Priority**: Very High  
**Description**: Prevents leaking internal error details to API clients.  
**Use When**: Reviewing or fixing error handling in API routes.

### service-role-key-protection
**Type**: Security  
**Priority**: Very High  
**Description**: Enforces the use of `createAdminClient()` instead of raw service role keys.  
**Use When**: Auditing or refactoring admin-level Supabase usage.

### strict-zod-schema-enforcement
**Type**: Security  
**Priority**: High  
**Description**: Replaces loose validation (`z.any()`) with strict, well-typed Zod schemas.  
**Use When**: Hardening input validation on API routes.
