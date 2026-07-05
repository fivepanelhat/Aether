#!/usr/bin/env python3
"""
Aether Orchestrator - Phase B (hardened)

Fixes over previous revision:
- Removed duplicate method definitions (register_skill, get_available_skills)
- Guardrails + ThreatModeler are now wired into the execution path
- Tool calls are logged exactly once (audit trail is accurate)
- max_steps=0 no longer raises NameError
- Skills directory resolved robustly (CWD -> env -> ~/.aether/skills)
"""

import logging
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from .memory import AetherMemory
from .guardrails import Guardrails
from .threat_modeling import ThreatModeler
from .tools import ToolRegistry, ToolExecutor, ToolCache
from .tools.base import ToolResult
from .skills.loader import SkillLoader
from .llm import OllamaClient, build_react_messages, parse_decision

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("AetherOrchestrator")


def _resolve_skills_directory(explicit: Optional[str] = None) -> Optional[str]:
    """
    Resolve the skills directory in priority order:
    1. Explicit argument
    2. AETHER_SKILLS_DIR environment variable
    3. ./skills relative to the current working directory
    4. ~/.aether/skills
    Returns the first existing directory, or None.
    """
    candidates = []
    if explicit:
        candidates.append(explicit)
    env_dir = os.environ.get("AETHER_SKILLS_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append(os.path.join(os.getcwd(), "skills"))
    candidates.append(os.path.join(os.path.expanduser("~"), ".aether", "skills"))

    for candidate in candidates:
        if candidate and os.path.isdir(candidate):
            return candidate
    return None


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
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    history: List[str] = field(default_factory=list)
    cultural_considerations: List[str] = field(default_factory=list)

    def summarize(self) -> str:
        summary = f"Goal: {self.goal}\nPhase: {self.current_phase}\n"
        if self.plan:
            summary += "Plan:\n" + "\n".join(f"  - {p}" for p in self.plan) + "\n"
        summary += f"Loaded Skills: {', '.join(self.loaded_skills) if self.loaded_skills else 'None'}\n"
        return summary


class AetherOrchestrator:
    def __init__(self, memory_path: Optional[str] = None, skills_directory: Optional[str] = None,
                 llm: Optional[OllamaClient] = None, use_llm: bool = True):
        self.state: Optional[TaskState] = None
        self.memory = AetherMemory(persist_path=memory_path)
        self.guardrails = Guardrails()
        self.threat_modeler = ThreatModeler()
        self.llm = llm or OllamaClient()
        self.use_llm = use_llm

        # Tool system
        self.tool_registry = ToolRegistry()
        self.tool_cache = ToolCache(default_ttl=300)  # 5 minutes
        self.tool_executor = ToolExecutor(self.tool_registry, cache=self.tool_cache)
        self._register_default_tools()

        # === Dynamic Skill Loading ===
        resolved = _resolve_skills_directory(skills_directory)
        if resolved:
            self.skill_loader = SkillLoader(skills_directory=resolved)
            self.skills_registry = self.skill_loader.load_all_skills()
        else:
            self.skill_loader = None
            self.skills_registry = {}
            logger.warning(
                "No skills directory found. Searched: explicit arg, $AETHER_SKILLS_DIR, "
                "./skills, ~/.aether/skills. Running in core mode."
            )

        logger.info(f"AetherOrchestrator initialized with {len(self.skills_registry)} skills")

    # ==================== Skill Registry ====================

    def register_skill(self, name: str, metadata: Dict[str, Any]):
        """Manually register a skill (useful for testing or runtime addition)."""
        self.skills_registry[name] = metadata
        logger.info(f"Manually registered skill: {name}")

    def get_available_skills(self) -> List[str]:
        return list(self.skills_registry.keys())

    def get_skill_info(self, name: str) -> Optional[Dict[str, Any]]:
        return self.skills_registry.get(name)

    # ==================== Tool Registry ====================

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

    def get_available_tools(self) -> List[str]:
        return self.tool_registry.list_tool_names()

    def call_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool and record exactly one audit entry.
        Returns the full ToolResult (callers can inspect .success/.output/.error).
        """
        result = self.tool_executor.execute(tool_name, **kwargs)

        if self.state:
            self.state.tool_calls.append({
                "tool": tool_name,
                "success": result.success,
                "error": result.error,
                "cached": bool(result.metadata.get("cached")),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        return result

    # ==================== Skill Suggestion ====================

    def _suggest_skills(self, goal: str) -> List[str]:
        """
        Dynamic skill prioritization based on:
        - Keyword/tag matching
        - Skill type priority
        - Cultural sensitivity & HITL requirements
        - Whether the skill has already been loaded
        """
        goal_lower = goal.lower()
        scored_skills = []

        for skill_name, meta in self.skills_registry.items():
            if self.state and skill_name in self.state.loaded_skills:
                continue

            score = 0
            tags = meta.get("tags", [])
            skill_type = meta.get("type", "")
            requires_hitl = meta.get("requires_hitl", False)
            cultural_sensitivity = meta.get("cultural_sensitivity", "low")

            for tag in tags:
                if tag in goal_lower:
                    score += 3

            if skill_type in ["security", "orchestration"]:
                score += 4
            elif skill_type in ["workflow", "hygiene"]:
                score += 2

            if requires_hitl:
                score += 2

            if cultural_sensitivity in ["medium", "high"]:
                if any(kw in goal_lower for kw in ["cultural", "maori", "whanau", "community"]):
                    score += 3

            if score > 0:
                scored_skills.append((skill_name, score))

        scored_skills.sort(key=lambda x: x[1], reverse=True)
        return [skill[0] for skill in scored_skills]

    def start_task(self, goal: str) -> TaskState:
        self.state = TaskState(goal=goal)
        self.state.history.append(f"Task started: {goal}")
        logger.info(f"Task started: {goal}")

        # Cultural sensitivity assessment at task start (wired guardrail)
        sensitivity = self.guardrails.assess_cultural_sensitivity(goal)
        if sensitivity != "low":
            note = f"Cultural sensitivity assessed as '{sensitivity}' for this goal."
            self.state.cultural_considerations.append(note)
            logger.info(note)

        suggested = self._suggest_skills(goal)
        self.state.suggested_skills = suggested
        if suggested:
            logger.info(f"Suggested skills: {suggested}")

        return self.state

    def load_skill(self, skill_name: str):
        if self.state and skill_name in self.skills_registry:
            if skill_name not in self.state.loaded_skills:
                self.state.loaded_skills.append(skill_name)
                self.state.history.append(f"Loaded skill: {skill_name}")
                logger.info(f"Loaded skill: {skill_name}")

    # ==================== Pipeline Loop ====================
    # NOTE: This is a deterministic, rule-based pipeline. It will become a true
    # ReAct loop once LLM inference (Ollama) is wired into _generate_thought /
    # _decide_next_action in Phase C. Named honestly until then.

    def run_pipeline(self, goal: str, max_steps: int = 8) -> TaskState:
        """
        Deterministic task pipeline with tools, skills, guardrail-backed
        approval gates, error handling, and accurate audit logging.
        """
        self.start_task(goal)
        logger.info(f"Starting pipeline for goal: {goal}")

        steps_taken = 0
        for step in range(max_steps):
            steps_taken = step + 1
            try:
                thought = self._generate_thought()
                action = self._decide_next_action(thought, goal)

                if action == "conclude":
                    logger.info("[Pipeline] Task complete.")
                    break

                # Approval gate — now backed by Guardrails + ThreatModeler
                if self._requires_approval(action, context=goal):
                    logger.warning(f"[Pipeline] '{action}' requires human approval. Stopping.")
                    self.state.history.append(f"Pending approval for: {action}")
                    break

                if action in self.tool_registry.list_tool_names():
                    # call_tool records the audit entry — do not append again here
                    self.call_tool(action, query=goal)

                elif action in self.skills_registry:
                    self.load_skill(action)
                    skill_result = self._execute_skill(action, goal)
                    self.state.tool_calls.append({
                        "step": steps_taken,
                        "type": "skill",
                        "name": action,
                        "result": skill_result,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })

            except Exception as e:
                logger.error(f"[Pipeline] Error at step {steps_taken}: {e}")
                self.state.tool_calls.append({
                    "step": steps_taken,
                    "type": "error",
                    "message": str(e),
                })
                break

        self.state.current_phase = "pipeline_complete"
        logger.info(f"Pipeline finished after {steps_taken} steps")
        return self.state

    # ==================== Real ReAct Loop (Phase C) ====================

    def run_react_loop(self, goal: str, max_steps: int = 8, auto_remediate: bool = False) -> TaskState:
        """
        LLM-driven ReAct loop (Ollama). Each step: the model reasons over the
        goal, state, tools, skills, and recent observations, then chooses ONE
        action. Guardrails + ThreatModeler gate high-risk actions before
        execution. Falls back to the deterministic pipeline if Ollama is
        unreachable.
        """
        if not self.use_llm or not self.llm.is_available():
            logger.warning("LLM unavailable - falling back to deterministic pipeline.")
            return self.run_pipeline(goal, max_steps=max_steps)

        self.start_task(goal)
        logger.info(f"Starting ReAct loop (model: {self.llm.model}) for goal: {goal}")

        observations: List[str] = []
        allowed = self.get_available_tools() + self.get_available_skills() + ["conclude"]
        skill_descriptions = "\n".join(
            f"- {name}: {meta.get('description', '')}" for name, meta in self.skills_registry.items()
        ) or "No skills loaded."

        steps_taken = 0
        for step in range(max_steps):
            steps_taken = step + 1
            try:
                messages = build_react_messages(
                    goal=goal,
                    state_summary=self.state.summarize(),
                    tool_descriptions=self.tool_registry.get_tool_descriptions(),
                    skill_descriptions=skill_descriptions,
                    observations=observations,
                )
                raw = self.llm.chat(messages)
                decision = parse_decision(raw, allowed_actions=allowed)

                suspicious, patterns = self.guardrails.detect_prompt_injection(decision.thought)
                if suspicious:
                    logger.warning(f"[ReAct] Injection patterns in model thought: {patterns}. Concluding.")
                    self.state.history.append(f"Halted: injection patterns detected {patterns}")
                    break

                if not decision.valid:
                    logger.warning(f"[ReAct] Invalid decision: {decision.error}")
                    observations.append(
                        f"Step {steps_taken}: your last response was invalid ({decision.error}). Respond with valid JSON."
                    )
                    continue

                self.state.history.append(f"Thought {steps_taken}: {decision.thought}")
                self.memory.add_entry("thought", decision.thought, {"step": steps_taken, "goal": goal})
                logger.info(f"[ReAct] Step {steps_taken} thought: {decision.thought[:120]}")

                if decision.action == "conclude":
                    logger.info("[ReAct] Model concluded the task.")
                    break

                if self._requires_approval(decision.action, context=goal):
                    logger.warning(f"[ReAct] '{decision.action}' requires human approval. Stopping.")
                    self.state.history.append(f"Pending approval for: {decision.action}")
                    break

                if decision.action in self.tool_registry.list_tool_names():
                    result = self.call_tool(decision.action, **decision.args)
                    obs = result.output if result.success else f"ERROR: {result.error}"
                    observations.append(f"Step {steps_taken} [{decision.action}]: {str(obs)[:800]}")
                    self.memory.add_entry(
                        "tool_result",
                        str(obs)[:2000],
                        {"tool": decision.action, "success": result.success},
                    )

                elif decision.action in self.skills_registry:
                    self.load_skill(decision.action)
                    skill_result = self._execute_skill(decision.action, goal)
                    body = self.skills_registry[decision.action].get("body", "")
                    observations.append(
                        f"Step {steps_taken} [skill:{decision.action}] instructions:\n{body[:1200]}"
                    )
                    self.state.tool_calls.append({
                        "step": steps_taken,
                        "type": "skill",
                        "name": decision.action,
                        "result": skill_result,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })

            except Exception as e:
                logger.error(f"[ReAct] Error at step {steps_taken}: {e}")
                self.state.tool_calls.append({"step": steps_taken, "type": "error", "message": str(e)})
                break

        self.state.current_phase = "react_complete"
        self.memory.add_entry("task_complete", goal, {"steps": steps_taken, "phase": "react_complete"})
        logger.info(f"ReAct loop finished after {steps_taken} steps")
        return self.state

    def _decide_next_action(self, thought: str, goal: str) -> str:
        tool_calls_count = len(self.state.tool_calls)

        if tool_calls_count >= 7:
            return "conclude"

        suggested_skills = self._suggest_skills(goal)
        if suggested_skills and not self.state.loaded_skills:
            return suggested_skills[0]

        available_tools = self.tool_registry.list_tool_names()

        if "codebase_search" in available_tools and tool_calls_count < 2:
            return "codebase_search"

        if "memory_query" in available_tools and tool_calls_count < 3:
            return "memory_query"

        if "directory_lister" in available_tools and tool_calls_count < 4:
            return "directory_lister"

        if any(kw in goal.lower() for kw in ["create", "write", "implement", "generate", "build"]):
            if "file_writer" in available_tools:
                return "file_writer"

        return "conclude"

    def _generate_thought(self) -> str:
        return f"Actions taken so far: {len(self.state.tool_calls)}"

    # ==================== Safe Execution Layer ====================

    def _requires_approval(self, action: str, context: str = "") -> bool:
        """
        Single source of truth: Guardrails owns the approval policy,
        ThreatModeler provides a second, independent signal.
        """
        if self.guardrails.enforce_hitl(action, context):
            return True
        threat_model = self.threat_modeler.analyze_action(action, context)
        return threat_model.requires_hitl

    def request_approval(self, action: str, details: str = "") -> bool:
        print("\n" + "=" * 70)
        print("AETHER — HUMAN APPROVAL REQUIRED")
        print("=" * 70)
        print(f"Action: {action}")
        if details:
            print(f"Details: {details}")
        print("\nThis action is considered high-risk.")
        response = input("Do you want to proceed? (yes/no): ").strip().lower()
        return response in ["yes", "y"]

    def execute_action_safely(self, action: str, **kwargs) -> dict:
        """Execute high-risk actions only after approval."""
        if self._requires_approval(action, context=str(kwargs)):
            approved = self.request_approval(action, str(kwargs))
            if not approved:
                logger.warning(f"User denied execution of: {action}")
                if self.state:
                    self.state.history.append(f"User rejected action: {action}")
                return {"executed": False, "reason": "User rejected action"}

        result = self.call_tool(action, **kwargs)
        if result.success:
            if self.state:
                self.state.history.append(f"Executed safely: {action}")
            # Invalidate search cache after any write so results stay fresh
            if action == "file_writer":
                self.tool_cache.invalidate("codebase_search")
            return {"executed": True, "result": result.output}

        logger.error(f"Execution failed: {result.error}")
        return {"executed": False, "error": result.error}

    def safe_write_file(self, file_path: str, content: str, mode: str = "write") -> dict:
        """Safe wrapper for writing files with approval gate."""
        return self.execute_action_safely(
            "file_writer",
            file_path=file_path,
            content=content,
            mode=mode
        )

    # ==================== Skill Execution ====================

    def _execute_skill(self, skill_name: str, goal: str):
        logger.info(f"[Skill Execution] Running: {skill_name}")

        if skill_name not in self.skills_registry:
            logger.warning(f"Skill '{skill_name}' not found in registry.")
            return {"skill": skill_name, "applied": False, "error": "Skill not found in registry"}

        skill_meta = self.skills_registry[skill_name]
        instructions = skill_meta.get("body", "No instructions found.")

        if self.state:
            self.state.history.append(
                f"Loaded instructions for skill '{skill_name}':\n{instructions}"
            )

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
    state = aether.run_pipeline(
        "Explore the current codebase and suggest improvements for the agent system"
    )
    print(aether.summarize())
