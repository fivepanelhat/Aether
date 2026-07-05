#!/usr/bin/env python3
"""
Aether Orchestrator - Phase B
With structured logging and improved skill registration.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

import os
from .memory import AetherMemory
from .guardrails import Guardrails
from .tools import ToolRegistry, ToolExecutor, ToolCache
from .skills.loader import SkillLoader

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
    cultural_considerations: List[str] = field(default_factory=list)

    def summarize(self) -> str:
        summary = f"Goal: {self.goal}\nPhase: {self.current_phase}\n"
        if self.plan:
            summary += "Plan:\n" + "\n".join(f"  - {p}" for p in self.plan) + "\n"
        summary += f"Loaded Skills: {', '.join(self.loaded_skills) if self.loaded_skills else 'None'}\n"
        return summary


class AetherOrchestrator:
    def __init__(self, memory_path: Optional[str] = None):
        self.state: Optional[TaskState] = None
        self.memory = AetherMemory(persist_path=memory_path)
        self.guardrails = Guardrails()

        # Tool system
        self.tool_registry = ToolRegistry()
        self.tool_cache = ToolCache(default_ttl=300)  # 5 minutes
        self.tool_executor = ToolExecutor(self.tool_registry, cache=self.tool_cache)
        self._register_default_tools()

        # === Dynamic Skill Loading ===
        self.skill_loader = SkillLoader(skills_directory="skills")
        self.skills_registry = self.skill_loader.load_all_skills()

        if self.skills_registry:
            print(f"[Aether] Loaded {len(self.skills_registry)} skills.")
        else:
            print("[Aether] No skills loaded. You can add skills in the 'skills/' folder.")

        logger.info(f"AetherOrchestrator initialized with {len(self.skills_registry)} skills")

    def register_skill(self, name: str, metadata: Dict[str, Any]):
        """Manually register a skill (useful for testing or runtime addition)."""
        self.skills_registry[name] = metadata
        logger.info(f"Manually registered skill: {name}")

    def get_available_skills(self) -> List[str]:
        return list(self.skills_registry.keys())

    def get_skill_info(self, name: str) -> Optional[Dict[str, Any]]:
        return self.skills_registry.get(name)

    def _register_default_tools(self):
        from .tools.file_reader import FileReaderTool
        from .tools.codebase_search import CodebaseSearchTool
        from .tools.memory_query import MemoryQueryTool
        from .tools.file_writer import FileWriterTool
        from .tools.directory_lister import DirectoryListerTool

        self.tool_registry.register(FileReaderTool())
        self.tool_registry.register(CodebaseSearchTool())
        self.tool_registry.register(FileWriterTool())
        self.tool_registry.register(DirectoryListerTool())

        memory_tool = MemoryQueryTool()
        memory_tool.memory = self.memory
        self.tool_registry.register(memory_tool)

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

    # ==================== Final Strengthened ReAct Loop ====================

    def run_react_loop(self, goal: str, max_steps: int = 8) -> TaskState:
        """
        Final robust ReAct loop.
        Includes tools, skills, approval gates, error handling, and result tracking.
        """
        self.start_task(goal)
        logger.info(f"Starting ReAct loop for goal: {goal}")

        for step in range(max_steps):
            try:
                thought = self._generate_thought()
                action = self._decide_next_action(thought, goal)

                if action == "conclude":
                    logger.info("[ReAct] Task complete or max steps reached.")
                    break

                # Approval Gate
                if self._requires_approval(action):
                    logger.warning(f"[ReAct] '{action}' requires human approval. Stopping.")
                    self.state.history.append(f"Pending approval for: {action}")
                    break

                # Execute Tool
                if action in self.tool_registry.list_tool_names():
                    result = self.call_tool(action, query=goal)
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "tool",
                        "name": action,
                        "success": result.success if hasattr(result, "success") else True
                    })

                # Execute Skill
                elif action in self.skills_registry:
                    self.load_skill(action)
                    skill_result = self._execute_skill(action, goal)
                    self.state.tool_calls.append({
                        "step": step + 1,
                        "type": "skill",
                        "name": action,
                        "result": skill_result
                    })

            except Exception as e:
                logger.error(f"[ReAct] Error at step {step + 1}: {e}")
                self.state.tool_calls.append({
                    "step": step + 1,
                    "type": "error",
                    "message": str(e)
                })
                break

        self.state.current_phase = "react_complete"
        logger.info(f"ReAct loop finished after {step + 1} steps")
        return self.state

    def _decide_next_action(self, thought: str, goal: str) -> str:
        tool_calls_count = len(self.state.tool_calls)

        if tool_calls_count >= 7:
            return "conclude"

        # Dynamic skill prioritization
        suggested_skills = self._suggest_skills(goal)
        if suggested_skills and not self.state.loaded_skills:
            return suggested_skills[0]

        available_tools = self.tool_registry.list_tool_names()

        # Information gathering tools first
        if "codebase_search" in available_tools and tool_calls_count < 2:
            return "codebase_search"

        if "memory_query" in available_tools and tool_calls_count < 3:
            return "memory_query"

        if "directory_lister" in available_tools and tool_calls_count < 4:
            return "directory_lister"

        # Execution tools
        if any(kw in goal.lower() for kw in ["create", "write", "implement", "generate", "build"]):
            if "file_writer" in available_tools:
                return "file_writer"

        return "conclude"

    def _generate_thought(self) -> str:
        return f"Actions taken so far: {len(self.state.tool_calls)}"

    # ==================== Enhanced Safe Execution Layer ====================

    def _requires_approval(self, action: str) -> bool:
        high_risk = {"file_writer", "git_commit", "git_push", "deploy", "delete_data"}
        return action in high_risk

    def request_approval(self, action: str, details: str = "") -> bool:
        """
        Interactive approval prompt.
        In a real CLI this would pause and wait for user input.
        """
        print("\n" + "="*70)
        print("AETHER — HUMAN APPROVAL REQUIRED")
        print("="*70)
        print(f"Action: {action}")
        if details:
            print(f"Details: {details}")
        print("\nThis action is considered high-risk.")
        response = input("Do you want to proceed? (yes/no): ").strip().lower()
        return response in ["yes", "y"]

    def execute_action_safely(self, action: str, **kwargs) -> dict:
        """Execute high-risk actions only after approval."""
        if self._requires_approval(action):
            approved = self.request_approval(action, str(kwargs))
            if not approved:
                logger.warning(f"User denied execution of: {action}")
                if self.state:
                    self.state.history.append(f"User rejected action: {action}")
                return {"executed": False, "reason": "User rejected action"}

        try:
            result = self.call_tool(action, **kwargs)
            if self.state:
                self.state.history.append(f"Executed safely: {action}")
            return {"executed": True, "result": result}
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {"executed": False, "error": str(e)}

    def safe_write_file(self, file_path: str, content: str, mode: str = "write") -> dict:
        """Safe wrapper for writing files with approval gate."""
        return self.execute_action_safely(
            "file_writer",
            file_path=file_path,
            content=content,
            mode=mode
        )

    # ==================== Skill Execution (All Skills) ====================

    def _execute_skill(self, skill_name: str, goal: str):
        logger.info(f"[Skill Execution] Running: {skill_name}")

        if skill_name not in self.skills_registry:
            logger.warning(f"Skill '{skill_name}' not found in registry.")
            return {"skill": skill_name, "applied": False, "error": "Skill not found in registry"}
            
        skill_meta = self.skills_registry[skill_name]
        
        # Inject the instructions into the context
        instructions = skill_meta.get("body", "No instructions found.")
        
        if self.state:
            self.state.history.append(f"Loaded instructions for skill '{skill_name}':\n{instructions}")
        
        return {
            "skill": skill_name,
            "applied": True,
            "notes": [f"Instructions loaded into context. Agent must follow the instructions for '{skill_name}'."]
        }

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
