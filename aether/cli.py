#!/usr/bin/env python3
"""
Aether CLI - Improved Output Formatting
"""

import argparse
import sys
from aether.orchestrator import AetherOrchestrator


def print_header(text: str):
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70)


def print_section(title: str, content: str):
    print(f"\n[{title}]")
    print(content)


def run_task(goal: str, max_steps: int = 8, memory_path: str = None):
    print_header("AETHER TASK")

    print(f"Goal: {goal}")
    print(f"Max Steps: {max_steps}")

    aether = AetherOrchestrator(memory_path=memory_path)
    state = aether.run_react_loop(goal=goal, max_steps=max_steps)

    print_section("Summary", state.summarize())

    if hasattr(state, "skill_execution_results") and state.skill_execution_results:
        print("\n[Skill Execution Results]")
        for res in state.skill_execution_results:
            print(f"  Skill: {res.get('skill')}")
            for note in res.get("notes", []):
                print(f"    - {note}")

    print("\n[Recent Activity]")
    for entry in state.history[-10:]:
        print(f"  {entry}")

    print("\n" + "="*70)
    print("Task completed.")
    print("="*70 + "\n")

    return state


def list_skills():
    aether = AetherOrchestrator()
    print_header("AVAILABLE SKILLS")

    for name, meta in aether.skills_registry.items():
        desc = meta.get("description", "No description")
        skill_type = meta.get("type", "general")
        hitl = "Yes" if meta.get("requires_hitl") else "No"
        print(f"  {name}")
        print(f"    Type: {skill_type} | Requires Approval: {hitl}")
        try:
            print(f"    {desc}\n")
        except UnicodeEncodeError:
            clean_desc = desc.encode("ascii", "ignore").decode("ascii")
            print(f"    {clean_desc}\n")


def main():
    parser = argparse.ArgumentParser(description="Aether - Sovereign Agentic Development System")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a task")
    run_parser.add_argument("goal", type=str, help="Task goal")
    run_parser.add_argument("--max-steps", type=int, default=8)
    run_parser.add_argument("--memory", type=str, default=None)

    subparsers.add_parser("skills", help="List available skills")

    args = parser.parse_args()

    if args.command == "run":
        run_task(args.goal, args.max_steps, args.memory)
    elif args.command == "skills":
        list_skills()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
