import os
import re
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("AetherSkillLoader")

class SkillLoader:
    def __init__(self):
        self.skills_registry: Dict[str, Dict[str, Any]] = {}
        # Matches YAML frontmatter between --- and ---
        self.frontmatter_pattern = re.compile(r"^---\s*(.*?)\s*---", re.DOTALL | re.MULTILINE)

    def discover_skills(self, skills_dir: str) -> Dict[str, Dict[str, Any]]:
        """
        Scans a directory for SKILL.md files, parses them, and returns a registry
        of discovered skills.
        """
        skills_path = Path(skills_dir)
        if not skills_path.exists() or not skills_path.is_dir():
            logger.warning(f"Skills directory not found: {skills_dir}")
            return self.skills_registry

        logger.info(f"Scanning for skills in {skills_dir}...")

        # Find all SKILL.md files in immediate subdirectories
        for skill_folder in skills_path.iterdir():
            if not skill_folder.is_dir():
                continue

            skill_file = skill_folder / "SKILL.md"
            if not skill_file.exists():
                continue

            parsed_skill = self._parse_skill_file(skill_file)
            if parsed_skill:
                skill_name = parsed_skill.get("name")
                if skill_name:
                    self.skills_registry[skill_name] = parsed_skill
                    logger.info(f"Loaded dynamic skill: {skill_name}")

        return self.skills_registry

    def _parse_skill_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        try:
            content = filepath.read_text(encoding="utf-8")
            match = self.frontmatter_pattern.match(content)

            if not match:
                logger.warning(f"No valid YAML frontmatter found in {filepath}")
                return None

            yaml_content = match.group(1)
            body = content[match.end():].strip()

            metadata = yaml.safe_load(yaml_content)

            if not isinstance(metadata, dict):
                logger.warning(f"Frontmatter in {filepath} is not a valid YAML dictionary")
                return None

            if "name" not in metadata or "description" not in metadata:
                logger.warning(f"Skill in {filepath} is missing required fields ('name', 'description')")
                return None

            # Add the markdown body to the metadata so it can be passed as instructions
            metadata["instructions"] = body
            metadata["filepath"] = str(filepath)

            return metadata

        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in {filepath}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading skill file {filepath}: {e}")
            return None
