---
name: release-engineering
description: Manages versioning, tagging, builds, smoke testing, and release processes in a consistent and reliable way.
version: "0.1.0"
type: workflow
requires_hitl: true
cultural_sensitivity: low
tags: [release, versioning, ci, build, deploy, tagging]
---

# Release Engineering

## Overview
This skill standardizes the process of preparing, building, testing, tagging, and releasing software. It covers version bumps, desktop builds, smoke testing, and ensuring releases are clean and reproducible.

## When to Use
- Preparing a new release or version bump.
- Building desktop installers (e.g. Tauri, Electron).
- Running smoke tests before tagging or deploying.
- Creating Git tags and pushing releases.
- Ensuring CI is green and the release is properly documented.

## Instructions

### 1. Versioning
- Decide on the new version number following semantic versioning.
- Update `package.json`, `pyproject.toml`, or equivalent version files.
- Update changelogs or release notes if applicable.

### 2. Build & Verification
- Run a clean production build (`npm run build` or equivalent).
- Ensure all tests pass (unit + E2E).
- Run smoke tests against the built application or preview deployment.

### 3. Desktop Builds (if applicable)
- Build desktop installers using the project's build system (e.g. Tauri).
- Verify that installers are generated for the required platforms (Windows, macOS, Linux).
- Check installer sizes and basic functionality.

### 4. Git & Release Process
- Commit all release-related changes with a clear message.
- Create and push a Git tag (e.g. `v0.4.0`).
- Push the tag to trigger any release workflows (e.g. GitHub Actions for building installers).

### 5. Post-Release Checks
- Verify the release appears correctly on GitHub Releases.
- Confirm desktop installers are attached and downloadable.
- Update any documentation or demo links if needed.

## Guardrails & Constraints
- All releases must have green CI (type-check, lint, tests, build).
- Desktop installers should be built via CI when possible for reproducibility.
- Never tag a release if smoke tests are failing.
- Requires human approval before tagging and pushing releases (`requires_hitl: true`).

## Input / Output

**Input**: A decision to prepare a new release or version. 
**Output**: A clean, tagged, and verified release with all necessary artifacts (web build + desktop installers).

## Examples

**Before**: Manual tagging, inconsistent desktop builds, missing smoke tests, and releases pushed with failing CI.

**After**: Structured release process with version bump -> clean build -> smoke tests -> tag -> CI-generated installers -> verified release.

## References
- Project CI/CD workflows (e.g. `.github/workflows`)
- Tauri or desktop build configuration
- Previous release commits and tags in the project history
