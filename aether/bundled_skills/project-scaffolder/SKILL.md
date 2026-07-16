---
name: project-scaffolder
description: Scaffolds new projects or major features following best practices. Use this when the user wants to initialize a new Next.js project, set up a new feature module, or bootstrap a consistent project structure with Tailwind, shadcn/ui, and proper conventions.
version: "0.1.0"
type: workflow
requires_hitl: true
cultural_sensitivity: low
tags: [scaffolding, bootstrap, project, nextjs, setup, initialization]
---

# Project Scaffolder

## Overview
This skill helps initialize new projects or major features with a clean, consistent structure. It is designed to reduce repetitive setup work while enforcing good architectural patterns.

## When to Use
- The user wants to start a new Next.js project.
- The user wants to scaffold a new major feature or module inside an existing project.
- The user asks to "set up", "bootstrap", or "initialize" a project or feature.
- A new repository or significant new section of the codebase needs to be created from scratch.

## Instructions

### 1. Clarify Requirements
Before scaffolding, confirm the following with the user:
- Is this a **new project** or a **new feature/module** inside an existing project?
- What framework/stack should be used? (Default: Next.js 15 + App Router + TypeScript + Tailwind + shadcn/ui)
- Are there any specific requirements (e.g. Supabase, authentication, specific folder structure)?

### 2. Determine Scope
Decide whether to scaffold:
- A full new project, or
- Just a feature/module inside an existing codebase

### 3. Create Project Structure
When creating a new project, generate the following structure by default:

```text
<project-name>/
|-- app/
| |-- (auth)/
| | |-- login/page.tsx
| | `-- register/page.tsx
| |-- (dashboard)/
| | `-- dashboard/page.tsx
| |-- api/
| | `-- health/route.ts
| |-- layout.tsx
| |-- page.tsx
| `-- globals.css
|-- components/
| |-- ui/ # shadcn/ui components
| `-- shared/ # Shared application components
|-- lib/
| |-- utils.ts
| |-- supabase/
| | |-- client.ts
| | `-- server.ts
| `-- validations/ # Zod schemas
|-- types/
| `-- index.ts
|-- public/
|-- .env.local.example
|-- .eslintrc.json
|-- tailwind.config.ts
|-- tsconfig.json
|-- next.config.ts
`-- package.json
```

### 4. Follow Established Conventions
- Use the existing component patterns from `hub-nextjs-component` skill where applicable.
- Include proper TypeScript typing.
- Set up accessible defaults (WCAG 2.2 AA considerations).
- Include a basic error boundary and loading states.
- Add security-minded defaults (e.g. proper environment variable handling).

### 5. Generate Key Files
Create the following files with sensible defaults:
- `app/layout.tsx` (with metadata and basic structure)
- `app/page.tsx` (clean starting page)
- `app/globals.css` (with Tailwind and basic design tokens)
- `.env.example` (with common variables)
- `README.md` for the new project

### 6. Output the Result
- Clearly list all files and folders that were created.
- Provide the user with next steps (e.g. `cd` into the folder, install dependencies, run the dev server).

## Guardrails & Constraints
- **Always require human approval** before writing files to disk (use the approval system).
- Do not overwrite existing files without explicit confirmation.
- Prefer creating a new directory rather than modifying an existing project unless the user specifically asks for it.
- Follow the project's established conventions for components, styling, and structure.

## Input / Output

**Input**: A request to scaffold a new project or feature, including any specific requirements. 
**Output**: A well-structured project or feature with clear next steps for the user.

## Examples

**Example 1:** 
Input: "Scaffold a new Next.js project for a resource directory" 
Output: Creates a new folder with proper structure, layout, basic components, and Tailwind setup.

**Example 2:** 
Input: "Create the folder structure for a new admin dashboard feature" 
Output: Creates the relevant folders and files inside the existing project.

