---
name: schema-migration-hygiene
description: Detects schema drift and creates safe, targeted database migrations (including performance indexes).
version: "0.1.0"
type: hygiene
requires_hitl: true
cultural_sensitivity: medium
---

# Schema & Migration Hygiene

## Overview
Prevents silent runtime failures caused by missing columns/tables and ensures good database performance through proper indexing.

## When to Use
- Code references columns or tables that don't exist in migrations
- Queries are slow due to missing indexes
- New features require database changes

## Instructions
1. Compare code usage against current migrations.
2. Create targeted migrations for missing columns/indexes.
3. Add performance indexes on frequently filtered/sorted columns.
4. Verify migrations cleanly (ideally with Docker or a test DB).
5. Document any schema changes.

## Guardrails & Constraints
- All migrations must be reviewed before applying to production.
- Prefer additive, non-destructive changes.
- Index vector columns with HNSW when using pgvector for RAG.
- Requires human approval (`requires_hitl: true`).
