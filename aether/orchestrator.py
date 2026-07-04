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
            "design-system-unification": {"description": "Unifies design tokens and component styling", "tags": ["design", "ui", "theme", "consistency"]},
            "release-engineering": {"description": "Manages versioning, builds, testing, and releases", "tags": ["release", "versioning", "ci", "build", "deploy", "tagging"]},
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
        """
        Dynamic skill prioritization based on multiple factors:
        - Keyword/tag matching
        - Skill type priority
        - Cultural sensitivity & HITL requirements
        - Whether the skill has already been loaded
        """
        goal_lower = goal.lower()
        scored_skills = []

        for skill_name, meta in self.skills_registry.items():
            if self.state and skill_name in self.state.loaded_skills:
                continue  # Skip already loaded skills

            score = 0
            tags = meta.get("tags", [])
            skill_type = meta.get("type", "")
            requires_hitl = meta.get("requires_hitl", False)
            cultural_sensitivity = meta.get("cultural_sensitivity", "low")

            # 1. Tag / Keyword matching (base score)
            for tag in tags:
                if tag in goal_lower:
                    score += 3

            # 2. Boost high-impact skill types
            if skill_type in ["security", "orchestration"]:
                score += 4
            elif skill_type in ["workflow", "hygiene"]:
                score += 2

            # 3. Prioritize skills that require HITL (they are often critical)
            if requires_hitl:
                score += 2

            # 4. Slightly boost culturally sensitive skills when relevant
            if cultural_sensitivity in ["medium", "high"]:
                if any(kw in goal_lower for kw in ["cultural", "maori", "whanau", "community"]):
                    score += 3

            if score > 0:
                scored_skills.append((skill_name, score))

        # Sort by score descending (highest priority first)
        scored_skills.sort(key=lambda x: x[1], reverse=True)

        # Return only skill names, sorted by priority
        return [skill[0] for skill in scored_skills]

    def load_skill(self, skill_name: str):
        if self.state and skill_name in self.skills_registry:
            if skill_name not in self.state.loaded_skills:
                self.state.loaded_skills.append(skill_name)
                self.state.history.append(f"Loaded skill: {skill_name}")
                logger.info(f"Loaded skill: {skill_name}")

    # ==================== Safe Execution Layer ====================

    def execute_with_approval(self, action: str, **kwargs) -> bool:
        """
        Execute high-risk actions only after checking approval requirements.
        Currently logs a warning and blocks execution.
        """
        if self._requires_approval(action):
            logger.warning(f"Action '{action}' requires human approval. Execution blocked.")
            if self.state:
                self.state.history.append(f"Blocked execution of: {action} (pending approval)")
            return False

        # If no approval needed, proceed with tool execution
        try:
            result = self.call_tool(action, **kwargs)
            return result.success if hasattr(result, 'success') else True
        except Exception as e:
            logger.error(f"Execution failed for {action}: {e}")
            return False

    # Example: Controlled file writing
    def safe_write_file(self, file_path: str, content: str) -> bool:
        """Safe wrapper around file writing with approval gate."""
        return self.execute_with_approval("file_writer", file_path=file_path, content=content)

    # ==================== Improved Decision Logic ====================

    def run_react_loop(self, goal: str, max_steps: int = 8) -> TaskState:
        """
        ReAct loop that supports:
        - Tool calling
        - Skill loading + basic execution
        - Approval gates
        """
        self.start_task(goal)
        logger.info(f"Starting ReAct loop for: {goal}")

        for step in range(max_steps):
            thought = self._generate_thought()
            action = self._decide_next_action(thought, goal)

            if action == "conclude":
                logger.info("[ReAct] Concluding loop.")
                break

            # === Approval Gate ===
            if self._requires_approval(action):
                logger.warning(f"[ReAct] Action '{action}' requires human approval. Stopping.")
                self.state.history.append(f"Pending approval for: {action}")
                break

            # === Execute Tool ===
            if action in self.tool_registry.list_tool_names():
                try:
                    logger.info(f"[ReAct] Calling tool: {action}")
                    result = self.call_tool(action, query=goal)
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action,
                        "success": True
                    })
                except Exception as e:
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action,
                        "success": False,
                        "error": str(e)
                    })

            # === Load + Execute Skill ===
            elif action in self.skills_registry:
                logger.info(f"[ReAct] Loading and executing skill: {action}")
                self.load_skill(action)

                # Basic skill execution hook (we can expand this later)
                self._execute_skill(action, goal)

                self.state.tool_calls.append({
                    "step": step + 1,
                    "type": "skill",
                    "name": action
                })

        self.state.current_phase = "react_complete"
        logger.info(f"ReAct loop finished after {step + 1} steps")
        return self.state

    def _execute_skill(self, skill_name: str, goal: str):
        """
        Placeholder for executing skill-specific logic.
        For now it just logs. We will expand this per skill.
        """
        logger.info(f"[Skill Execution] Running logic for skill: {skill_name}")
        self.state.history.append(f"Executed skill logic: {skill_name}")

        # Example: You can add skill-specific behavior here later
        if skill_name == "agent-reliability-context":
            self.state.history.append("Applied agent reliability improvements (simulated)")

    def _generate_thought(self) -> str:
        return f"Actions taken: {len(self.state.tool_calls)}"

    def _decide_next_action(self, thought: str, goal: str) -> str:
        tool_calls_count = len(self.state.tool_calls)

        if tool_calls_count >= 7:
            return "conclude"

        # Use dynamic skill prioritization
        suggested_skills = self._suggest_skills(goal)
        if suggested_skills and not self.state.loaded_skills:
            return suggested_skills[0]  # Highest priority skill first

        # Then fall back to tools
        available_tools = self.tool_registry.list_tool_names()

        if "codebase_search" in available_tools and tool_calls_count < 2:
            return "codebase_search"

        if "memory_query" in available_tools and tool_calls_count < 3:
            return "memory_query"

        if any(kw in goal.lower() for kw in ["create", "write", "implement", "generate"]):
            if "file_writer" in available_tools:
                return "file_writer"

        return "conclude"

    def _requires_approval(self, action: str) -> bool:
        """High-risk actions that require human approval."""
        return action in {"file_writer", "git_commit", "git_push", "deploy"}

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
