#!/usr/bin/env bash
# Validate a single skill directory.
# Mirrors the rules used by the official skill validator + adds CAT versioning checks.
#
# Usage:
#   validate-skill.sh <skill-directory>
#
set -euo pipefail

die() { echo "FAIL: $*" >&2; exit 1; }
ok()  { echo "OK: $*"; }

[[ $# -ne 1 ]] && die "Usage: validate-skill.sh <skill-directory>"

SKILL_DIR="$1"
SKILL_MD="$SKILL_DIR/SKILL.md"
EXPECTED_NAME=$(basename "$SKILL_DIR")

[[ -d "$SKILL_DIR" ]] || die "Directory does not exist: $SKILL_DIR"
[[ -f "$SKILL_MD" ]]  || die "SKILL.md not found in $SKILL_DIR"

CONTENT=$(<"$SKILL_MD")

# Frontmatter delimiter
if [[ "$CONTENT" != ---* ]]; then
  die "SKILL.md must start with --- (YAML frontmatter)"
fi

FRONTMATTER=$(echo "$CONTENT" | awk '/^---$/{n++; next} n==1')
[[ -n "$FRONTMATTER" ]] || die "Empty or malformed frontmatter"

BODY=$(echo "$CONTENT" | awk '/^---$/{n++; next} n>=2')
BODY_TRIMMED=$(echo "$BODY" | sed '/^[[:space:]]*$/d')
[[ -n "$BODY_TRIMMED" ]] || die "SKILL.md body is empty"

# name
NAME_LINE=$(echo "$FRONTMATTER" | grep -m1 '^name:' || true)
[[ -n "$NAME_LINE" ]] || die "Missing 'name' in frontmatter"
NAME_RAW=$(echo "$NAME_LINE" | sed 's/^name:[[:space:]]*//')
if [[ "$NAME_RAW" =~ ^\".*\"$ ]] || [[ "$NAME_RAW" =~ ^\'.*\'$ ]]; then
  die "'name' must not be wrapped in quotes"
fi
NAME="$NAME_RAW"

[[ ${#NAME} -ge 2 && ${#NAME} -le 64 ]] || die "Name length invalid"
if echo "$NAME" | grep -qE '\-\-'; then
  die "Name contains consecutive hyphens"
fi
if ! echo "$NAME" | grep -qE '^[a-z0-9][a-z0-9-]*[a-z0-9]$'; then
  die "Name '$NAME' is invalid — use lowercase a-z, digits, single hyphens; start/end with alnum"
fi
if [[ "$NAME" != "$EXPECTED_NAME" ]]; then
  die "Name '$NAME' must match directory name '$EXPECTED_NAME'"
fi

# description
DESC_LINE=$(echo "$FRONTMATTER" | grep -m1 '^description:' || true)
[[ -n "$DESC_LINE" ]] || die "Missing 'description' in frontmatter"
DESC_RAW=$(echo "$DESC_LINE" | sed 's/^description:[[:space:]]*//')
if [[ "$DESC_RAW" =~ ^\".*\"$ ]] || [[ "$DESC_RAW" =~ ^\'.*\'$ ]] || [[ "$DESC_RAW" =~ ^\" ]] || [[ "$DESC_RAW" =~ ^\' ]]; then
  die "'description' must be a plain (unquoted) YAML scalar"
fi
DESCRIPTION="$DESC_RAW"
[[ -n "$DESCRIPTION" ]] || die "'description' is empty"
if echo "$DESCRIPTION" | grep -qi 'TODO'; then
  die "Description still contains 'TODO'"
fi
if echo "$DESCRIPTION" | grep -q ': '; then
  die "Description contains ': ' (colon-space) — reword"
fi
if echo "$DESCRIPTION" | grep -qE '[<>]'; then
  die "Description contains angle brackets — reword"
fi
DESC_LEN=${#DESCRIPTION}
if [[ "$DESC_LEN" -gt 1024 ]]; then
  die "Description too long ($DESC_LEN chars, max 1024)"
fi

# Allowed top-level fields only
ALLOWED_FIELDS="name description license compatibility metadata allowed-tools"
while IFS= read -r line; do
  if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_-]*)[[:space:]]*: ]]; then
    KEY="${BASH_REMATCH[1]}"
    if ! echo " $ALLOWED_FIELDS " | grep -q " $KEY "; then
      die "Unknown frontmatter field '$KEY' — put custom keys under 'metadata:'"
    fi
  fi
done <<< "$FRONTMATTER"

# Tokenizer control tokens
CONTROL_HITS=$(grep -REn '<\|[A-Za-z][A-Za-z0-9_-]*\|>' --include='*.md' "$SKILL_DIR" 2>/dev/null || true)
if [[ -n "$CONTROL_HITS" ]]; then
  echo "$CONTROL_HITS" | head -5 >&2
  die "Found tokenizer control token(s) shaped like <|...|> — remove them"
fi

# Versioning (recommended for CAT skills)
if echo "$FRONTMATTER" | grep -q '^metadata:'; then
  if echo "$FRONTMATTER" | grep -q 'version:'; then
    ok "metadata.version present"
  else
    echo "WARN: metadata present but no 'version' field (recommended for CAT skills)"
  fi
else
  echo "WARN: no metadata block — version tracking not enabled for this skill"
fi

# CHANGELOG recommendation when versioned
if echo "$FRONTMATTER" | grep -q 'version:'; then
  if [[ -f "$SKILL_DIR/references/CHANGELOG.md" ]] || [[ -f "$SKILL_DIR/CHANGELOG.md" ]]; then
    ok "CHANGELOG present"
  else
    echo "WARN: versioned skill has no CHANGELOG.md (recommended under references/)"
  fi
fi

LINE_COUNT=$(echo "$CONTENT" | wc -l | tr -d ' ')
ok "Skill '$NAME' is valid ($LINE_COUNT lines)"