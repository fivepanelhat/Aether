# Changelog — aether-skill-authoring

## [1.2.0] — 2026-07-27

### Added
- Mandatory lifecycle metadata: `status` (`active` | `experimental` | `deprecated`) and `owner`.
- Documented selection behaviour for each status value (deprecated skills excluded from default shortlists).
- New reference: `references/anti-sprawl.md` (standing rules, pre-creation checklist, composition & trajectory discipline, retirement guidance).
- Anti-sprawl items added to the validation checklist and anti-patterns.

### Changed
- Frontmatter Rules section expanded to cover both description quality and lifecycle metadata.
- Version bumped to 1.2.0; source_insights updated to include AI Agent Sprawl governance patterns.

## [1.1.1] — 2026-07-26

### Added
- Explicit guidance that description quality is critical for correct Tier-1 triggering.
- New reference: `references/industry-practices.md` capturing progressive-disclosure tiers, procedural-memory framing, skills-vs-tools relationship, and security posture from IBM Technology and the emerging open standard.
- Security note: treat skills containing scripts like software dependencies.

### Changed
- Strengthened Frontmatter Rules section with precision requirement for descriptions.
- Updated validation checklist and anti-patterns to include vague descriptions.
- Bumped version and source_insights to include IBM Technology video.

## [1.1.0] — 2026-07-26

### Added
- Progressive disclosure as a non-negotiable design rule (metadata → body → references).
- Preferred authoring method: Successful real run → agent writes the skill.
- Explicit recursive improvement loop (feed failure → update skill).
- Validation checklist before shipping a skill.
- Source insights from Greg Isenberg + Ras Mic (progressive disclosure & skill creation) and HyperAgent/Howie Liu (skills as key primitive).

### Changed
- Strengthened description requirements and token-efficiency focus.
- Clarified HITL and cultural safety integration points.
- Updated frontmatter version and last_updated.

### Removed
- Generic / theoretical-only authoring guidance that encouraged writing skills without lived successful runs.
