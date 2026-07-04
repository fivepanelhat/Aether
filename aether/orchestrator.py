#!/usr/bin/env python3
"""
Aether Orchestrator - Phase B
With structured logging and improved skill registration.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from memory import AetherMemory
from guardrails import Guardrails
from tools import ToolRegistry, ToolExecutor, ToolCache

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("AetherOrchestrator")


@dataclass
class TaskState:
    goal: str
    plan: List[str] = field(default_factory=list)
    suggested_skills: List[str] = field(default_factory=list)
    loaded_skills: List[str] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    proposed_changes: List[Dict[str, Any]] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    current_phase: str = "planning"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    history: List[str] = field(default_factory=list)


class AetherOrchestrator:
    def __init__(self, memory_path: Optional[str] = None):
        self.state: Optional[TaskState] = None
        self.memory = AetherMemory(persist_path=memory_path)
        self.guardrails = Guardrails()

        self.tool_registry = ToolRegistry()
        self.tool_cache = ToolCache(default_ttl=300)  # 5 minutes
        self.tool_executor = ToolExecutor(self.tool_registry, cache=self.tool_cache)
        self._register_default_tools()

        self.skills_registry: Dict[str, Dict[str, Any]] = {}
        self._register_default_skills()

        logger.info("AetherOrchestrator initialized")

    def _register_default_tools(self):
        from tools.file_reader import FileReaderTool
        from tools.codebase_search import CodebaseSearchTool
        from tools.memory_query import MemoryQueryTool
        from tools.file_writer import FileWriterTool

        self.tool_registry.register(FileReaderTool())
        self.tool_registry.register(CodebaseSearchTool())
        self.tool_registry.register(FileWriterTool())

        memory_tool = MemoryQueryTool()
        memory_tool.memory = self.memory
        self.tool_registry.register(memory_tool)

    def _register_default_skills(self):
        default_skills = {
            "hub-nextjs-component": {"description": "Builds accessible UI components", "tags": ["ui", "component"]},
            "security-auth-guard": {"description": "Adds auth and role guards to routes", "tags": ["security", "auth"]},
            "agent-reliability-context": {"description": "Improves agent context and reliability", "tags": ["agent", "context"]},
            "build-ci-hygiene": {"description": "Fixes build and CI issues", "tags": ["build", "ci"]},
            "schema-migration-hygiene": {"description": "Handles schema drift and migrations", "tags": ["database", "migration"]},
        }
        for name, meta in default_skills.items():
            self.register_skill(name, meta)

    def register_skill(self, name: str, metadata: Dict[str, Any]):
        self.skills_registry[name] = metadata

    def get_available_skills(self) -> List[str]:
        return list(self.skills_registry.keys())

    def get_available_tools(self) -> List[str]:
        return self.tool_registry.list_tool_names()

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        result = self.tool_executor.execute(tool_name, **kwargs)

        if self.state:
            self.state.tool_calls.append({
                "tool": tool_name,
                "success": result.success,
                "output": result.output if result.success else None,
                "error": result.error
            })

        if result.success:
            return result.output
        else:
            raise RuntimeError(f"Tool '{tool_name}' failed: {result.error}")

    def _select_tools_for_goal(self, goal: str) -> List[str]:
        goal_lower = goal.lower()
        selected = []

        if any(kw in goal_lower for kw in ["existing", "pattern", "codebase", "search"]):
            selected.append("codebase_search")
        if any(kw in goal_lower for kw in ["memory", "previous", "past"]):
            selected.append("memory_query")
        if any(kw in goal_lower for kw in ["create", "write", "generate", "implement"]):
            selected.append("file_writer")

        return selected

    def start_task(self, goal: str) -> TaskState:
        self.state = TaskState(goal=goal)
        self.state.history.append(f"Task started: {goal}")
        logger.info(f"Task started: {goal}")

        suggested = self._suggest_skills(goal)
        self.state.suggested_skills = suggested

        if suggested:
            logger.info(f"Suggested skills: {suggested}")

        return self.state

    def _suggest_skills(self, goal: str) -> List[str]:
        """Suggest relevant skills based on goal keywords and tags."""
        goal_lower = goal.lower()
        suggestions = []

        for skill_name, meta in self.skills_registry.items():
            tags = meta.get("tags", [])
            if any(tag in goal_lower for tag in tags):
                suggestions.append(skill_name)

        # Remove already loaded skills
        if self.state:
            suggestions = [s for s in suggestions if s not in self.state.loaded_skills]

        return suggestions

    def load_skill(self, skill_name: str):
        if self.state and skill_name in self.skills_registry:
            if skill_name not in self.state.loaded_skills:
                self.state.loaded_skills.append(skill_name)
                self.state.history.append(f"Loaded skill: {skill_name}")
                logger.info(f"Loaded skill: {skill_name}")

    def execute_file_write(self, file_path: str, content: str) -> bool:
        """Safe file writing with HITL gate."""
        if self.guardrails.enforce_hitl("file_write"):
            logger.warning("File write requires human approval.")
            self.state.history.append(f"Pending approval for writing to: {file_path}")
            return False

        try:
            result = self.call_tool("file_writer", file_path=file_path, content=content)
            self.state.history.append(f"Wrote to file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"File write failed: {e}")
            return False

    def run_react_loop(self, goal: str, max_steps: int = 8) -> TaskState:
        self.start_task(goal)

        for step in range(max_steps):
            thought = self._generate_thought()
            action = self._decide_next_action(thought, goal)

            if action == "conclude":
                break

            # Execute Tool
            if action in self.tool_registry.list_tool_names():
                try:
                    result = self.call_tool(action, query=goal)
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action
                    })
                except Exception as e:
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action,
                        "error": str(e)
                    })

            # Load Skill
            elif action in self.skills_registry:
                self.load_skill(action)
                self.state.tool_calls.append({
                    "step": step + 1,
                    "type": "skill",
                    "name": action
                })

        self.state.current_phase = "react_complete"
        return self.state

    def _generate_thought(self) -> str:
        return f"Current actions taken: {len(self.state.tool_calls)}"

    def _decide_next_action(self, thought: str, goal: str) -> str:
        tool_calls_count = len(self.state.tool_calls)

        if tool_calls_count >= 6:
            return "conclude"

        # Prioritize loading a relevant skill early
        suggested_skills = self._suggest_skills(goal)
        if suggested_skills and not self.state.loaded_skills:
            return suggested_skills[0]

        # Then use tools for information gathering
        if "codebase_search" in self.tool_registry.list_tool_names() and tool_calls_count < 2:
            return "codebase_search"

        if "memory_query" in self.tool_registry.list_tool_names() and tool_calls_count < 3:
            return "memory_query"

        return "conclude"

    def summarize(self) -> str:
        if not self.state:
            return "No active task."

        return f"""
=== AETHER TASK ===
Goal: {self.state.goal}
Phase: {self.state.current_phase}
Suggested Skills: {self.state.suggested_skills}
Loaded Skills: {self.state.loaded_skills}
Tool Calls: {len(self.state.tool_calls)}
"""

if __name__ == "__main__":
    aether = AetherOrchestrator()

    state = aether.run_react_loop(
        "Explore the current codebase and suggest improvements for the agent system"
    )

    print(aether.summarize())
