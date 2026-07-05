"""
Dynamic Skill Loader for Aether

Scans the skills/ directory, parses SKILL.md files, and registers them.
"""

import os
import yaml
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("AetherSkillLoader")


class SkillLoader:
    def __init__(self, skills_directory: str = "skills"):
        self.skills_directory = skills_directory
        self.loaded_skills: Dict[str, Dict[str, Any]] = {}

    def load_all_skills(self) -> Dict[str, Dict[str, Any]]:
        """
        Scan the skills directory and load all valid skills.
        Returns a dictionary of skill_name -> skill_metadata.
        """
        if not os.path.exists(self.skills_directory):
            logger.warning(f"Skills directory not found: {self.skills_directory}")
            return {}

        self.loaded_skills = {}

        for item in os.listdir(self.skills_directory):
            skill_path = os.path.join(self.skills_directory, item)

            if not os.path.isdir(skill_path):
                continue

            skill_md_path = os.path.join(skill_path, "SKILL.md")

            if not os.path.exists(skill_md_path):
                continue

            try:
                skill_data = self._parse_skill_file(skill_md_path, item)
                if skill_data:
                    self.loaded_skills[skill_data["name"]] = skill_data
                    logger.info(f"Loaded skill: {skill_data['name']}")
            except Exception as e:
                logger.error(f"Failed to load skill from {item}: {e}")

        logger.info(f"Successfully loaded {len(self.loaded_skills)} skills")
        return self.loaded_skills

    def _parse_skill_file(self, file_path: str, folder_name: str) -> Optional[Dict[str, Any]]:
        """
        Parse a SKILL.md file and extract metadata from YAML frontmatter.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split frontmatter and body
        if not content.startswith("---"):
            logger.warning(f"No YAML frontmatter found in {file_path}")
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            logger.warning(f"Invalid frontmatter format in {file_path}")
            return None

        frontmatter = parts[1].strip()
        body = parts[2].strip()

        try:
            metadata = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {file_path}: {e}")
            return None

        if not isinstance(metadata, dict):
            logger.warning(f"Frontmatter is not a valid dictionary in {file_path}")
            return None

        # Validate required fields
        required_fields = ["name", "description"]
        for field in required_fields:
            if field not in metadata:
                logger.warning(f"Missing required field '{field}' in {file_path}")
                return None

        # Build skill data structure
        skill_data = {
            "name": metadata["name"],
            "description": metadata["description"],
            "version": metadata.get("version", "0.1.0"),
            "type": metadata.get("type", "general"),
            "requires_hitl": metadata.get("requires_hitl", False),
            "cultural_sensitivity": metadata.get("cultural_sensitivity", "low"),
            "tags": metadata.get("tags", []),
            "folder_path": os.path.dirname(file_path),
            "body": body,                    # The actual instructions
            "raw_metadata": metadata         # Keep original for debugging
        }

        return skill_data

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a loaded skill by name."""
        return self.loaded_skills.get(name)

    def list_skill_names(self) -> List[str]:
        """Return list of loaded skill names."""
        return list(self.loaded_skills.keys())
