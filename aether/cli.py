#!/usr/bin/env python3
"""
Aether CLI
"""

import argparse
import sys
from aether.orchestrator import AetherOrchestrator

__version__ = "0.4.0"


def print_header(text: str):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def run_task(goal: str, max_steps: int = 8, memory_path: str = None):
    print("\n" + "=" * 70)
    print("AETHER".center(70))
    print("=" * 70)
    print(f"Goal: {goal}")
    print(f"Max Steps: {max_steps}")
    print("-" * 70)

    try:
        aether = AetherOrchestrator(memory_path=memory_path)
        state = aether.run_react_loop(goal=goal, max_steps=max_steps)

        print("\n[Summary]")
        print(state.summarize())

        if hasattr(state, "skill_execution_results") and state.skill_execution_results:
            print("\n[Skills Used]")
            for result in state.skill_execution_results:
                print(f"  - {result.get('skill')}")

        print("\n[Recent Activity]")
        for entry in state.history[-8:]:
            print(f"  {entry}")

    except Exception as e:
        print(f"\n[Error] {e}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Task finished.")
    print("=" * 70 + "\n")


def list_skills():
    try:
        aether = AetherOrchestrator()
        print_header("AVAILABLE SKILLS")

        skills = aether.get_available_skills()
        if not skills:
            print("No skills found. Make sure the 'skills/' directory exists.")
            return

        for name in skills:
            info = aether.get_skill_info(name) or {}
            desc = info.get("description", "No description")
            print(f"  {name}")
            try:
                print(f"    {desc}\n")
            except UnicodeEncodeError:
                clean_desc = desc.encode("ascii", "ignore").decode("ascii")
                print(f"    {clean_desc}\n")

    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Aether - Sovereign Agentic Development System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a task using the ReAct loop")
    run_parser.add_argument("goal", type=str, help="The goal or task to work on")
    run_parser.add_argument("--max-steps", type=int, default=8, help="Maximum reasoning steps")
    run_parser.add_argument("--memory", type=str, default=None, help="Path to memory file")

    # Skills command
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
