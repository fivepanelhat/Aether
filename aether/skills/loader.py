# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Dynamic Skill Loader for Aether (Sprint E)

- Scan skills/ directories
- Parse and validate SKILL.md
- Honour depends_on / dependencies for topological load order
- Soft-import Core resolve_skill_order when available
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger("AetherSkillLoader")

try:
    from coastal_alpine_core import resolve_skill_order  # Core ≥0.5.10
except ImportError:  # pragma: no cover
    resolve_skill_order = None  # type: ignore


def _local_topo(skills: Dict[str, Dict[str, Any]]) -> List[str]:
    """Minimal fallback if Core skill_graph is unavailable."""
    dep_map = {}
    for name, meta in skills.items():
        raw = meta.get("depends_on") or []
        if isinstance(raw, str):
            raw = [raw]
        dep_map[name] = [str(x) for x in raw if str(x) in skills]
    indegree = {n: len(dep_map[n]) for n in dep_map}
    ready = sorted(n for n, d in indegree.items() if d == 0)
    order: List[str] = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for m, deps in dep_map.items():
            if n in deps and m not in order:
                indegree[m] -= 1
                if indegree[m] == 0:
                    ready.append(m)
                    ready.sort()
    if len(order) != len(skills):
        logger.warning("Skill dependency cycle or unresolved deps; using registration order")
        return list(skills.keys())
    return order


class SkillLoader:
    def __init__(self, skills_directory: str = "skills"):
        self.skills_directory = skills_directory
        self.loaded_skills: Dict[str, Dict[str, Any]] = {}
        self.load_order: List[str] = []

    def load_all_skills(self) -> Dict[str, Dict[str, Any]]:
        self.loaded_skills = {}
        self.load_order = []

        if not os.path.isdir(self.skills_directory):
            logger.warning(
                "Skills directory '%s' not found. Aether continues in core mode.",
                self.skills_directory,
            )
            return self.loaded_skills

        skill_folders = [
            f
            for f in os.listdir(self.skills_directory)
            if os.path.isdir(os.path.join(self.skills_directory, f))
        ]

        if not skill_folders:
            logger.info("No skills found; running in core mode.")
            return self.loaded_skills

        for folder_name in skill_folders:
            skill_path = os.path.join(self.skills_directory, folder_name)
            skill_md_path = os.path.join(skill_path, "SKILL.md")
            if not os.path.isfile(skill_md_path):
                alt = os.path.join(skill_path, "skill.md")
                if os.path.isfile(alt):
                    skill_md_path = alt
                else:
                    continue

            try:
                skill_data = self._parse_and_validate_skill(skill_md_path, folder_name)
                if skill_data:
                    name = skill_data["name"]
                    self.loaded_skills[name] = skill_data
                    logger.info("Loaded skill: %s (folder: %s)", name, folder_name)
            except Exception as e:
                logger.error("Failed to load skill from folder '%s': %s", folder_name, e)

        try:
            if resolve_skill_order is not None:
                self.load_order = resolve_skill_order(self.loaded_skills)
            else:
                self.load_order = _local_topo(self.loaded_skills)
        except Exception as e:
            logger.warning("Skill graph resolution failed (%s); using dict order", e)
            self.load_order = list(self.loaded_skills.keys())

        # Rebuild dict in load order for downstream consumers
        ordered = {n: self.loaded_skills[n] for n in self.load_order if n in self.loaded_skills}
        for n, meta in self.loaded_skills.items():
            if n not in ordered:
                ordered[n] = meta
        self.loaded_skills = ordered

        logger.info(
            "Skill Loader finished. Loaded %d skills. Order: %s",
            len(self.loaded_skills),
            self.load_order,
        )
        return self.loaded_skills

    def _parse_and_validate_skill(
        self, file_path: str, folder_name: str
    ) -> Optional[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip().startswith("---"):
            logger.warning("Skill file missing YAML frontmatter: %s", file_path)
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            logger.warning("Invalid YAML frontmatter structure in: %s", file_path)
            return None

        frontmatter_raw = parts[1].strip()
        body = parts[2].strip()

        try:
            metadata = yaml.safe_load(frontmatter_raw)
        except yaml.YAMLError as e:
            logger.error("YAML parsing failed in %s: %s", file_path, e)
            return None

        if not isinstance(metadata, dict):
            logger.warning("Frontmatter is not a dictionary in: %s", file_path)
            return None

        if "name" not in metadata or not metadata["name"]:
            logger.warning("Missing required field 'name' in: %s", file_path)
            return None

        if "description" not in metadata or not metadata["description"]:
            logger.warning("Missing required field 'description' in: %s", file_path)
            return None

        name = metadata["name"]
        if name != folder_name:
            logger.warning(
                "Skill name '%s' does not match folder '%s'. Using frontmatter name.",
                name,
                folder_name,
            )

        nested = metadata.get("metadata") or {}

        def _field(key, default):
            return metadata[key] if key in metadata else nested.get(key, default)

        depends_raw = _field("depends_on", _field("dependencies", []))
        if isinstance(depends_raw, str):
            depends_on = [depends_raw]
        elif isinstance(depends_raw, list):
            depends_on = [str(x) for x in depends_raw]
        else:
            depends_on = []

        skill_data = {
            "name": name,
            "description": metadata["description"],
            "version": str(_field("version", "0.1.0")),
            "type": _field("type", "general"),
            "requires_hitl": bool(_field("requires_hitl", False)),
            "cultural_sensitivity": _field("cultural_sensitivity", "low"),
            "tags": _field("tags", []) if isinstance(_field("tags", []), list) else [],
            "depends_on": depends_on,
            "reversible": bool(_field("reversible", False)),
            "folder_path": os.path.dirname(file_path),
            "body": body,
            "raw_metadata": metadata,
        }

        return skill_data

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        return self.loaded_skills.get(name)

    def list_skill_names(self) -> List[str]:
        return list(self.load_order) if self.load_order else list(self.loaded_skills.keys())

    def reload_skills(self) -> Dict[str, Dict[str, Any]]:
        logger.info("Reloading all skills from disk...")
        return self.load_all_skills()
