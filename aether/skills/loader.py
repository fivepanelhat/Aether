"""
Dynamic Skill Loader for Aether (Refined Phase 1)

Responsibilities:
- Scan the skills/ directory
- Parse and validate SKILL.md files
- Register skills dynamically
- Provide good error handling and logging
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
        self.loaded_skills = {}

        if not os.path.isdir(self.skills_directory):
            logger.warning(
                f"Skills directory '{self.skills_directory}' not found.\n"
                "Aether will continue with core functionality only.\n"
                "Create the 'skills/' folder and add skills to unlock extended capabilities."
            )
            return self.loaded_skills

        skill_folders = [f for f in os.listdir(self.skills_directory) 
                         if os.path.isdir(os.path.join(self.skills_directory, f))]

        if not skill_folders:
            logger.warning(
                f"No skill folders found in '{self.skills_directory}'.\n"
                "Aether is running with no skills loaded."
            )
            return self.loaded_skills

        for folder_name in skill_folders:
            skill_path = os.path.join(self.skills_directory, folder_name)

            if not os.path.isdir(skill_path):
                continue

            skill_md_path = os.path.join(skill_path, "SKILL.md")

            if not os.path.isfile(skill_md_path):
                continue

            try:
                skill_data = self._parse_and_validate_skill(skill_md_path, folder_name)
                if skill_data:
                    name = skill_data["name"]
                    self.loaded_skills[name] = skill_data
                    logger.info(f"Loaded skill: {name} (from folder: {folder_name})")
            except Exception as e:
                logger.error(f"Failed to load skill from folder '{folder_name}': {e}")

        logger.info(f"Dynamic Skill Loader finished. Loaded {len(self.loaded_skills)} skills.")
        return self.loaded_skills

    def _parse_and_validate_skill(self, file_path: str, folder_name: str) -> Optional[Dict[str, Any]]:
        """
        Parse SKILL.md and perform basic validation.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip().startswith("---"):
            logger.warning(f"Skill file missing YAML frontmatter: {file_path}")
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            logger.warning(f"Invalid YAML frontmatter structure in: {file_path}")
            return None

        frontmatter_raw = parts[1].strip()
        body = parts[2].strip()

        try:
            metadata = yaml.safe_load(frontmatter_raw)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing failed in {file_path}: {e}")
            return None

        if not isinstance(metadata, dict):
            logger.warning(f"Frontmatter is not a dictionary in: {file_path}")
            return None

        # === Validation ===
        if "name" not in metadata or not metadata["name"]:
            logger.warning(f"Missing required field 'name' in: {file_path}")
            return None

        if "description" not in metadata or not metadata["description"]:
            logger.warning(f"Missing required field 'description' in: {file_path}")
            return None

        name = metadata["name"]

        # Warn if folder name and skill name don't match (but still allow it)
        if name != folder_name:
            logger.warning(
                f"Skill name '{name}' does not match folder name '{folder_name}'. "
                f"Using skill name from frontmatter."
            )

        # Type validation / normalization
        skill_data = {
            "name": name,
            "description": metadata["description"],
            "version": str(metadata.get("version", "0.1.0")),
            "type": metadata.get("type", "general"),
            "requires_hitl": bool(metadata.get("requires_hitl", False)),
            "cultural_sensitivity": metadata.get("cultural_sensitivity", "low"),
            "tags": metadata.get("tags", []) if isinstance(metadata.get("tags"), list) else [],
            "folder_path": os.path.dirname(file_path),
            "body": body,
            "raw_metadata": metadata
        }

        return skill_data

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a loaded skill by name."""
        return self.loaded_skills.get(name)

    def list_skill_names(self) -> List[str]:
        """Return list of all loaded skill names."""
        return list(self.loaded_skills.keys())

    def reload_skills(self) -> Dict[str, Dict[str, Any]]:
        """Reload all skills from disk. Useful during development."""
        logger.info("Reloading all skills from disk...")
        return self.load_all_skills()
