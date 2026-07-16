---
name: aether-skills-ci
description: Use when creating, validating, testing, versioning, or setting up CI/CD for Aether or Coastal Alpine Tech skills. Handles skill frontmatter validation, semver enforcement, CHANGELOG requirements, pytest-based automated testing, and GitHub Actions workflow for skills. Trigger phrases include skills CI, validate skill, skill versioning, skills pipeline, test skills, skill catalog.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-11"
---

# Aether Skills CI

Production-grade continuous integration, validation, and automated testing for Aether and Coastal Alpine Tech skills.

## When to Use

- Validating a skill before commit or PR
- Adding versioning / CHANGELOG to a skill
- Setting up or updating the skills CI pipeline in a repository
- Running automated tests against skills
- Generating a skills catalog
- Reviewing or improving skill quality gates

## Core Capabilities

### 1. Validate a Skill
```bash
bash scripts/validate-skill.sh /path/to/skill-directory
```
Checks:
- Frontmatter structure and allowed fields
- `name` matches directory name
- `description` rules (plain scalar, length, no banned characters)
- Presence of `metadata.version` (recommended for CAT/Aether skills)
- CHANGELOG for versioned skills

### 2. Version Checks Across Skills
```bash
python3 scripts/check-skill-versions.py
```

### 3. Automated Tests
```bash
pip install -r references/requirements-test.txt
python -m pytest tests/ -v
```

### 4. Generate Skills Catalog
```bash
python3 scripts/generate-skills-catalog.py
```

### 5. Install CI into a Repository
Copy the following into the target repo (usually Aether or a skills monorepo):

```
.github/workflows/skills-ci.yml   ← from references/skills-ci.yml
scripts/validate-skill.sh
scripts/check-skill-versions.py
scripts/generate-skills-catalog.py
tests/                            ← full test suite + fixtures
requirements-test.txt
```

Recommended layout in the target repo:
```
skills/
  cat-architectural-standards/
  aether-core/
  ...
.github/workflows/skills-ci.yml
scripts/
tests/
```

## Versioning Convention (Enforced)

Every CAT / Aether skill should declare:

```yaml
metadata:
  version: "1.0.0"
  status: active
  last_updated: "YYYY-MM-DD"
```

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Bump on any material change to behaviour or definitions
- Maintain `references/CHANGELOG.md`

## Integration with Other Skills

- Load `aether-core` first for HITL and orchestration rules
- Load `aether-skill-authoring` when creating or updating skills
- Load `cat-architectural-standards` when classifying work into Gold / Platinum / Diamond
- Use this skill whenever the task involves skill quality, CI, testing, or release safety of skills

## HITL

- Never push CI configuration or skill changes that affect production without explicit approval
- Present proposed workflow files and validation results for review before committing

## References

- `references/README.md` — full pipeline documentation
- `references/skills-ci.yml` — ready-to-use GitHub Actions workflow
- `references/requirements-test.txt` — test dependencies
- `scripts/` — validation and catalog scripts
- `tests/` — pytest suite + fixtures

## Current Status

- `cat-architectural-standards` v1.0.0 is fully compliant and covered by regression tests
- All validation and test tooling is production-ready
- 9 automated tests currently passing

---

Coastal Alpine Tech · Aether  
aether-skills-ci v1.0.0 · 11 July 2026