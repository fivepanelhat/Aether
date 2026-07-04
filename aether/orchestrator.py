#!/usr/bin/env python3
"""
Aether Orchestrator - Phase B
With improved tracking, logging, and skill registration.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from .memory import AetherMemory
from .guardrails import Guardrails
from .tools import ToolRegistry, ToolExecutor


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
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
    cultural_considerations: List[str] = field(default_factory=list)
    current_phase: str = "planning"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    history: List[str] = field(default_factory=list)


class AetherOrchestrator:
    def __init__(self, memory_path: Optional[str] = None):
        self.state: Optional[TaskState] = None
        self.memory = AetherMemory(persist_path=memory_path)
        self.guardrails = Guardrails()

        # Tool system
        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.tool_registry)
        self._register_default_tools()

        # Skill Registry (more structured)
        self.skills_registry: Dict[str, Dict[str, Any]] = {}
        self._register_default_skills()

        logger.info("AetherOrchestrator initialized")

    # ==================== Tool Registration ====================

    def _register_default_tools(self):
        from .tools.file_reader import FileReaderTool
        from .tools.codebase_search import CodebaseSearchTool
        from .tools.memory_query import MemoryQueryTool
        from .tools.file_writer import FileWriterTool

        self.tool_registry.register(FileReaderTool())
        self.tool_registry.register(CodebaseSearchTool())
        self.tool_registry.register(FileWriterTool())

        memory_tool = MemoryQueryTool()
        memory_tool.memory = self.memory
        self.tool_registry.register(memory_tool)

        logger.info(f"Registered {len(self.tool_registry.list_tools())} tools")

    # ==================== Tool Execution ====================

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
        """Smart tool selection based on goal keywords."""
        goal_lower = goal.lower()
        selected = []

        if any(kw in goal_lower for kw in ["existing", "current", "pattern", "codebase", "already", "search"]):
            selected.append("codebase_search")
        if any(kw in goal_lower for kw in ["previous", "before", "memory", "past", "recall"]):
            selected.append("memory_query")
        if any(kw in goal_lower for kw in ["read", "inspect", "look at", "check file"]):
            selected.append("file_reader")
        if any(kw in goal_lower for kw in ["create", "write", "generate", "implement", "build"]):
            selected.append("file_writer")

        return selected

    # ==================== Skill Registration ====================

    def _register_default_skills(self):
        """Register core skills with metadata."""
        default_skills = {
            "hub-nextjs-component": {
                "description": "Builds accessible UI components following Hub standards",
                "tags": ["ui", "component", "frontend", "accessibility"],
                "requires_hitl": False
            },
            "security-auth-guard": {
                "description": "Adds authentication and role-based guards to sensitive routes",
                "tags": ["security", "auth", "api"],
                "requires_hitl": False
            },
            "agent-reliability-context": {
                "description": "Improves agent history, streaming, and tool usage",
                "tags": ["agent", "reliability", "context"],
                "requires_hitl": False
            },
            "build-ci-hygiene": {
                "description": "Fixes build/CI issues and prevents module-level crashes",
                "tags": ["build", "ci", "hygiene"],
                "requires_hitl": False
            },
            "schema-migration-hygiene": {
                "description": "Detects schema drift and creates safe migrations",
                "tags": ["database", "migration", "schema"],
                "requires_hitl": True
            },
        }

        for name, meta in default_skills.items():
            self.register_skill(name, meta)

        logger.info(f"Registered {len(self.skills_registry)} skills")

    def register_skill(self, name: str, metadata: Dict[str, Any]):
        """Register a new skill dynamically."""
        self.skills_registry[name] = metadata
        logger.info(f"Registered skill: {name}")

    def get_available_skills(self) -> List[str]:
        return list(self.skills_registry.keys())

    def get_skill_info(self, name: str) -> Optional[Dict[str, Any]]:
        return self.skills_registry.get(name)

    # ==================== Core Methods ====================

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
        goal_lower = goal.lower()
        suggestions = []

        for skill_name, meta in self.skills_registry.items():
            tags = meta.get("tags", [])
            if any(tag in goal_lower for tag in tags):
                suggestions.append(skill_name)

        return suggestions

    def load_skill(self, skill_name: str):
        if self.state and skill_name in self.skills_registry:
            if skill_name not in self.state.loaded_skills:
                self.state.loaded_skills.append(skill_name)
                self.state.history.append(f"Loaded skill: {skill_name}")
                logger.info(f"Loaded skill: {skill_name}")

    def create_plan(self) -> List[str]:
        if not self.state:
            return []

        # === Phase B: Intelligent Tool Selection ===
        tools_to_use = self._select_tools_for_goal(self.state.goal)

        for tool_name in tools_to_use:
            try:
                if tool_name == "codebase_search":
                    result = self.call_tool("codebase_search", query=self.state.goal, max_results=5)
                    self.state.tool_calls.append({"tool": tool_name, "results": len(result)})

                elif tool_name == "memory_query":
                    result = self.call_tool("memory_query", query=self.state.goal, limit=3)
                    self.state.tool_calls.append({"tool": tool_name, "results": len(result)})

            except Exception as e:
                self.state.tool_calls.append({"tool": tool_name, "error": str(e)})

        # === Generate Plan ===
        plan = [
            "1. Understand goal and gather context",
            "2. Load relevant skills",
            "3. Explore codebase and memory using tools",
            "4. Design solution with guardrails",
            "5. Generate changes",
            "6. Prepare review package"
        ]

        if self.state.tool_calls:
            plan.insert(1, f"   → Used {len(self.state.tool_calls)} tool(s) during planning")

        self.state.plan = plan
        self.state.current_phase = "plan_created"
        logger.info("Plan created")
        return plan

    def run_react_loop(self, goal: str, max_steps: int = 8) -> TaskState:
        """
        Enhanced ReAct loop that can use both tools and skills.
        Includes basic execution awareness (safe file writing path).
        """
        self.start_task(goal)
        logger.info(f"Starting ReAct loop for goal: {goal}")

        for step in range(max_steps):
            logger.info(f"\n[ReAct] Step {step + 1}/{max_steps}")

            # 1. Reason about current state
            thought = self._reason(goal)

            # 2. Decide next action (tool, skill, or conclude)
            action = self._decide_action(thought, goal)

            if action == "conclude":
                logger.info("[ReAct] Task complete or max steps reached.")
                break

            # 3. Execute action
            if action in self.tool_registry.list_tool_names():
                try:
                    logger.info(f"[ReAct] Calling tool: {action}")
                    result = self.call_tool(action, query=goal)
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action,
                        "result": str(result)[:200]  # truncate for logging
                    })
                except Exception as e:
                    logger.error(f"Tool call failed: {e}")

            elif action in self.skills_registry:
                logger.info(f"[ReAct] Loading skill: {action}")
                self.load_skill(action)
                self.state.tool_calls.append({
                    "step": step + 1,
                    "type": "skill",
                    "name": action
                })

            # 4. Check for execution actions (safe file writing)
            if action == "file_writer":
                if self.guardrails.enforce_hitl("file_write"):
                    logger.warning("[ReAct] File write requires human approval.")
                    self.state.history.append("File write blocked - awaiting approval")

        self.state.current_phase = "react_complete"
        logger.info(f"ReAct loop finished after {step + 1} steps")
        return self.state

    def _reason(self, goal: str) -> str:
        """Simple reasoning step."""
        if len(self.state.tool_calls) == 0:
            return "No information gathered yet. Should explore the codebase or memory."
        return f"Gathered {len(self.state.tool_calls)} actions so far."

    def _decide_action(self, thought: str, goal: str) -> str:
        """
        Decide next action: tool, skill, file write, or conclude.
        This can later be upgraded with LLM reasoning.
        """
        tool_calls_count = len(self.state.tool_calls)

        # Stop condition
        if tool_calls_count >= 5:
            return "conclude"

        # Prefer loading a relevant skill early
        suggested = self._suggest_skills(goal)
        if suggested and not self.state.loaded_skills:
            return suggested[0]

        # Then use tools
        available_tools = self.tool_registry.list_tool_names()
        if "codebase_search" in available_tools and tool_calls_count < 2:
            return "codebase_search"
        if "memory_query" in available_tools and tool_calls_count < 3:
            return "memory_query"

        # Execution path (safe file writing)
        if any(kw in goal.lower() for kw in ["create", "write", "implement", "generate"]):
            return "file_writer"

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
