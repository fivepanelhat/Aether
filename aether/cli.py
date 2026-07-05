#!/usr/bin/env python3
"""
Aether CLI
Command-line interface for running Aether tasks.
"""

import argparse
import sys
from aether.orchestrator import AetherOrchestrator


def run_task(goal: str, max_steps: int = 8, memory_path: str = None):
    """Run a task using the ReAct loop."""
    print(f"\n[Aether] Starting task: {goal}\n")

    aether = AetherOrchestrator(memory_path=memory_path)
    state = aether.run_react_loop(goal=goal, max_steps=max_steps)

    print("\n" + "="*60)
    print("TASK SUMMARY")
    print("="*60)
    print(state.summarize())

    if hasattr(state, "skill_execution_results") and state.skill_execution_results:
        print("\n[Skill Execution Results]")
        for result in state.skill_execution_results:
            print(f"  - {result.get('skill')}: {result.get('notes', [])}")

    print("\n[History Log]")
    for entry in state.history[-10:]:  # Show last 10 entries
        print(f"  {entry}")

    return state


def main():
    parser = argparse.ArgumentParser(
        description="Aether - Sovereign Agentic Development System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a task using the ReAct loop")
    run_parser.add_argument("goal", type=str, help="The goal/task to work on")
    run_parser.add_argument(
        "--max-steps", type=int, default=8,
        help="Maximum number of steps in the ReAct loop (default: 8)"
    )
    run_parser.add_argument(
        "--memory", type=str, default=None,
        help="Path to persist memory (optional)"
    )

    # List skills command
    skills_parser = subparsers.add_parser("skills", help="List available skills")

    args = parser.parse_args()

    if args.command == "run":
        run_task(
            goal=args.goal,
            max_steps=args.max_steps,
            memory_path=args.memory
        )
    elif args.command == "skills":
        aether = AetherOrchestrator()
        print("\nAvailable Skills:")
        for name, meta in aether.skills_registry.items():
            print(f"  - {name}: {meta.get('description', 'No description')}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
