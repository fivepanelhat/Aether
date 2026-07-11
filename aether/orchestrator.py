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
    """Delegate to aether.paths (includes packaged bundled_skills)."""
    from .paths import resolve_skills_directory

    return resolve_skills_directory(explicit)


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
    # Structured skill applications for CLI / audit (instructions injected into ReAct context)
    skill_execution_results: List[Dict[str, Any]] = field(default_factory=list)
    # Active skill instruction bodies the model must follow on subsequent steps
    active_skill_instructions: List[str] = field(default_factory=list)

    def summarize(self) -> str:
        summary = f"Goal: {self.goal}\nPhase: {self.current_phase}\n"
        if self.plan:
            summary += "Plan:\n" + "\n".join(f"  - {p}" for p in self.plan) + "\n"
        summary += f"Loaded Skills: {', '.join(self.loaded_skills) if self.loaded_skills else 'None'}\n"
        if self.active_skill_instructions:
            summary += (
                "\n--- BINDING SKILL PLAYBOOKS (must follow) ---\n"
                + "\n\n".join(self.active_skill_instructions)
                + "\n--- END PLAYBOOKS ---\n"
            )
        return summary


class AetherOrchestrator:
    def __init__(self, memory_path: Optional[str] = None, skills_directory: Optional[str] = None,
                 llm: Optional[OllamaClient] = None, use_llm: bool = True):
        self.state: Optional[TaskState] = None
        self.errors: List[str] = []
        self.auto_remediate: bool = False
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

        # Shared sandbox root: CWD at orchestrator construction (project boundary)
        root = os.getcwd()
        self.allowed_root = os.path.realpath(root)
        self.tool_registry.register(FileReaderTool(allowed_root=self.allowed_root))
        self.tool_registry.register(CodebaseSearchTool(allowed_root=self.allowed_root))
        self.tool_registry.register(FileWriterTool(allowed_root=self.allowed_root))
        self.tool_registry.register(DirectoryListerTool(allowed_root=self.allowed_root))

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

                # Approval gate — Guardrails + ThreatModeler; auto_remediate may proceed
                if not self._approve_if_needed(action, context=goal):
                    break

                if action in self.tool_registry.list_tool_names():
                    # call_tool records the audit entry — do not append again here
                    self.call_tool(action, **self._default_tool_kwargs(action, goal))

                elif action in self.skills_registry:
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
                self.errors.append(str(e))
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

        auto_remediate: when True, high-risk actions (e.g. file_writer) proceed
        without interactive approval (authorized batch / webhook mode). Default
        False preserves the safe halt-for-approval behaviour.
        """
        self.auto_remediate = bool(auto_remediate)

        if not self.use_llm or not self.llm.is_available():
            logger.warning("LLM unavailable - falling back to deterministic pipeline.")
            return self.run_pipeline(goal, max_steps=max_steps)

        self.start_task(goal)
        logger.info(
            f"Starting ReAct loop (model: {self.llm.model}, auto_remediate={self.auto_remediate}) "
            f"for goal: {goal}"
        )

        observations: List[str] = []
        allowed = self.get_available_tools() + self.get_available_skills() + ["conclude"]
        skill_descriptions = "\n".join(
            f"- {name}: {meta.get('description', '')}" for name, meta in self.skills_registry.items()
        ) or "No skills loaded."

        # Screen user goal once for injection patterns (not only model thoughts)
        goal_suspicious, goal_patterns = self.guardrails.detect_prompt_injection(goal)
        if goal_suspicious:
            logger.warning(f"[ReAct] Injection patterns in goal: {goal_patterns}")
            self.state.history.append(f"Goal flagged for injection patterns: {goal_patterns}")
            self.state.risks.append(f"prompt_injection:{','.join(goal_patterns)}")

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

                if not self._approve_if_needed(decision.action, context=goal):
                    break

                if decision.action in self.tool_registry.list_tool_names():
                    tool_args = decision.args or {}
                    # Fill missing required-ish kwargs from goal when model omits them
                    if not tool_args:
                        tool_args = self._default_tool_kwargs(decision.action, goal)
                    result = self.call_tool(decision.action, **tool_args)
                    obs = result.output if result.success else f"ERROR: {result.error}"
                    observations.append(f"Step {steps_taken} [{decision.action}]: {str(obs)[:800]}")
                    self.memory.add_entry(
                        "tool_result",
                        str(obs)[:2000],
                        {"tool": decision.action, "success": result.success},
                    )
                    if not result.success:
                        self.errors.append(f"{decision.action}: {result.error}")

                elif decision.action in self.skills_registry:
                    skill_result = self._execute_skill(decision.action, goal)
                    if skill_result.get("applied"):
                        # Full playbook lives in state.summarize() via active_skill_instructions;
                        # observation records application for the recent-obs window.
                        observations.append(
                            f"Step {steps_taken} [skill:{decision.action}]: playbook APPLIED. "
                            f"Follow ACTIVE SKILL PLAYBOOK '{decision.action}' in CURRENT STATE on all later steps. "
                            f"hitl={skill_result.get('requires_hitl')}, "
                            f"cultural={skill_result.get('cultural_sensitivity')}."
                        )
                    else:
                        observations.append(
                            f"Step {steps_taken} [skill:{decision.action}]: FAILED — "
                            f"{skill_result.get('error', 'unknown')}"
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
                self.errors.append(str(e))
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

    def _default_tool_kwargs(self, action: str, goal: str) -> Dict[str, Any]:
        """Sensible kwargs when the model/pipeline omits tool arguments."""
        if action == "codebase_search":
            return {"query": goal, "directory": "."}
        if action == "memory_query":
            return {"query": goal}
        if action == "directory_lister":
            return {"path": "."}
        if action == "file_reader":
            return {}
        if action == "file_writer":
            return {}
        return {}

    def _skill_requires_hitl(self, action: str) -> bool:
        """True when a registered skill declares HITL or high cultural sensitivity."""
        meta = self.skills_registry.get(action)
        if not meta:
            return False
        if meta.get("requires_hitl"):
            return True
        if str(meta.get("cultural_sensitivity", "low")).lower() == "high":
            return True
        return False

    def _requires_approval(self, action: str, context: str = "") -> bool:
        """
        Approval policy:
        - Guardrails (tool/keyword risk)
        - ThreatModeler (independent second signal)
        - Skill frontmatter: requires_hitl or cultural_sensitivity=high
        """
        if self.guardrails.enforce_hitl(action, context):
            return True
        threat_model = self.threat_modeler.analyze_action(action, context)
        if threat_model.requires_hitl:
            return True
        return self._skill_requires_hitl(action)

    def _approve_if_needed(self, action: str, context: str = "") -> bool:
        """
        Return True if the action may proceed.

        - Low-risk actions: proceed.
        - High-risk + auto_remediate: proceed (authorized batch mode).
        - High-risk + interactive TTY: prompt via request_approval.
        - High-risk + non-interactive (default): halt with pending approval.
        """
        if not self._requires_approval(action, context=context):
            return True

        if self.auto_remediate:
            logger.warning(f"[HITL] '{action}' authorized via auto_remediate=True")
            if self.state:
                self.state.history.append(f"Auto-remediate authorized: {action}")
            return True

        # Interactive approval only when stdin is a TTY (avoids hanging webhooks/tests)
        try:
            import sys
            if sys.stdin is not None and sys.stdin.isatty():
                approved = self.request_approval(action, details=context[:500] if context else "")
                if approved:
                    if self.state:
                        self.state.history.append(f"User approved action: {action}")
                    return True
                logger.warning(f"User denied execution of: {action}")
                if self.state:
                    self.state.history.append(f"User rejected action: {action}")
                return False
        except Exception as e:
            logger.debug(f"Interactive approval unavailable: {e}")

        logger.warning(f"'{action}' requires human approval. Stopping.")
        if self.state:
            self.state.history.append(f"Pending approval for: {action}")
        return False

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
        if not self._approve_if_needed(action, context=str(kwargs)):
            return {"executed": False, "reason": "Approval required or denied"}

        result = self.call_tool(action, **kwargs)
        if result.success:
            if self.state:
                self.state.history.append(f"Executed safely: {action}")
            # Invalidate search cache after any write so results stay fresh
            if action == "file_writer":
                self.tool_cache.invalidate("codebase_search")
            return {"executed": True, "result": result.output}

        logger.error(f"Execution failed: {result.error}")
        self.errors.append(f"{action}: {result.error}")
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

    def _skill_instruction_block(self, skill_name: str, body: str, max_chars: int = 3500) -> str:
        """Format skill body so the next ReAct turns treat it as binding playbook text."""
        clipped = body if len(body) <= max_chars else body[:max_chars] + "\n…[truncated]"
        return (
            f"### ACTIVE SKILL PLAYBOOK: {skill_name}\n"
            f"You MUST follow these instructions for remaining steps until the goal is met.\n"
            f"Prefer tools that implement the steps; do not skip HITL or cultural gates.\n\n"
            f"{clipped}"
        )

    def _execute_skill(self, skill_name: str, goal: str) -> Dict[str, Any]:
        """
        Apply a skill by injecting its SKILL.md body into task context.

        Skills are markdown playbooks (not sandboxed code). Application means:
        1. Register the skill as loaded
        2. Push a binding instruction block into active_skill_instructions (feeds summarize + ReAct)
        3. Record a structured skill_execution_results entry for CLI/audit
        """
        logger.info(f"[Skill Execution] Applying playbook: {skill_name}")

        if skill_name not in self.skills_registry:
            logger.warning(f"Skill '{skill_name}' not found in registry.")
            result = {
                "skill": skill_name,
                "applied": False,
                "error": "Skill not found in registry",
            }
            if self.state:
                self.state.skill_execution_results.append(result)
            return result

        skill_meta = self.skills_registry[skill_name]
        instructions = skill_meta.get("body") or "No instructions found."
        block = self._skill_instruction_block(skill_name, instructions)

        result = {
            "skill": skill_name,
            "applied": True,
            "requires_hitl": bool(skill_meta.get("requires_hitl")),
            "cultural_sensitivity": skill_meta.get("cultural_sensitivity", "low"),
            "version": skill_meta.get("version", "0.1.0"),
            "instruction_chars": len(instructions),
            "notes": [
                f"Playbook for '{skill_name}' injected into active skill context "
                f"(goal: {goal[:120]}{'…' if len(goal) > 120 else ''})."
            ],
        }

        if self.state:
            if skill_name not in self.state.loaded_skills:
                self.state.loaded_skills.append(skill_name)
            # Keep latest full block per skill (replace prior injection for same name)
            prefix = f"### ACTIVE SKILL PLAYBOOK: {skill_name}\n"
            self.state.active_skill_instructions = [
                b for b in self.state.active_skill_instructions if not b.startswith(prefix)
            ]
            self.state.active_skill_instructions.append(block)
            self.state.history.append(
                f"Applied skill playbook '{skill_name}' "
                f"({result['instruction_chars']} chars; "
                f"hitl={result['requires_hitl']}; "
                f"cultural={result['cultural_sensitivity']})"
            )
            self.state.skill_execution_results.append(result)
            self.memory.add_entry(
                "skill_applied",
                skill_name,
                {
                    "requires_hitl": result["requires_hitl"],
                    "cultural_sensitivity": result["cultural_sensitivity"],
                },
            )

        return result

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
