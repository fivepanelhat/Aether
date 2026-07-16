# Skills CI/CD Pipeline

Production-grade continuous integration and automated testing for Coastal Alpine Tech / Aether skills.

## Pipeline Overview

| Job | Purpose |
|-----|---------|
| **test** | Automated tests (pytest) for the validation tooling + regression tests against live skills |
| **validate-skills** | Structural frontmatter checks, semver + CHANGELOG enforcement, secret scan |
| **generate-catalog** | Auto-generated skills catalog (main branch only) |

## What is tested

### Automated Tests (`tests/`)
- Valid skill fixtures pass validation
- Invalid fixtures (wrong name, missing description) correctly fail
- Versioned skills are recognised
- Live `cat-architectural-standards` skill continues to validate (regression)

### Structural Validation
- Frontmatter rules (name matches directory, description constraints, allowed fields)
- Semver format on `metadata.version`
- CHANGELOG presence for versioned skills
- Lightweight secret pattern scan

## Local Usage

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run the full automated test suite
python -m pytest tests/ -v

# Validate a single skill
./scripts/validate-skill.sh skills/cat-architectural-standards
# or against the live skill:
./scripts/validate-skill.sh /home/workdir/.grok/skills/cat-architectural-standards

# Check versions across all skills
python3 scripts/check-skill-versions.py

# Generate catalog
python3 scripts/generate-skills-catalog.py
```

## Repository Layout Expected by CI

```text
.
├── .github/workflows/skills-ci.yml
├── scripts/
│   ├── validate-skill.sh
│   ├── check-skill-versions.py
│   └── generate-skills-catalog.py
├── tests/
│   ├── test_validate_skill.py
│   └── fixtures/
├── requirements-test.txt
└── skills/                    # recommended
    ├── cat-architectural-standards/
    │   ├── SKILL.md
    │   └── references/
    └── ...
```

## Versioning Convention (enforced)

```yaml
metadata:
  version: "1.0.0"          # required for CAT/Aether skills
  status: active
  last_updated: "YYYY-MM-DD"
```

- Bump version (semver) on any material change.
- Keep `references/CHANGELOG.md` for every versioned skill.

## Current Status

- `cat-architectural-standards` v1.0.0 is fully compliant and covered by regression tests.
- CI package is ready to be copied into the Aether (or dedicated skills) repository.

---

Coastal Alpine Tech · Aether  
Skills CI + Automated Testing · 11 July 2026
