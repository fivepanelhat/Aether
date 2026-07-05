#!/usr/bin/env python3
# Copyright 2026 Aether Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Aether CLI
"""

import argparse
import sys
from aether.orchestrator import AetherOrchestrator

__version__ = "0.1.0"


def print_header(text: str):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def run_task(goal: str, max_steps: int = 8, memory_path: str = None, auto_remediate: bool = False):
    print("\n" + "=" * 70)
    print("AETHER".center(70))
    print("=" * 70)
    print(f"Goal: {goal}")
    print(f"Max Steps: {max_steps}")
    print(f"Auto-Remediate: {auto_remediate}")
    print("-" * 70)

    try:
        aether = AetherOrchestrator(memory_path=memory_path)
        state = aether.run_react_loop(goal=goal, max_steps=max_steps, auto_remediate=auto_remediate)

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
    run_parser.add_argument("--auto-remediate", action="store_true", help="Authorize Aether to automatically fix issues, create branches, and run tests")

    # Skills command
    subparsers.add_parser("skills", help="List available skills")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize Aether in the current project (coming soon)")

    # Remediate command
    remediate_parser = subparsers.add_parser("remediate", help="Trigger the error remediation workflow on a specific error or CI failure")
    remediate_parser.add_argument("error", type=str, help="The error or CI failure to remediate")

    try:
        args = parser.parse_args()

        if not hasattr(args, "command") or not args.command:
            parser.print_help()
            sys.exit(1)

        if args.command == "run":
            if not args.goal or args.goal.strip() == "":
                print("Error: Please provide a goal. Example:\n  aether run \"Audit the API routes\"")
                sys.exit(1)
            run_task(args.goal, args.max_steps, args.memory, getattr(args, "auto_remediate", False))
        elif args.command == "skills":
            list_skills()
        elif args.command == "remediate":
            if not getattr(args, "error", "") or args.error.strip() == "":
                print("Error: Please provide an error. Example:\n  aether remediate \"CI failed on main branch\"")
                sys.exit(1)
            goal = f"Remediate the following error using error-remediation-orchestrator: {args.error}"
            run_task(goal, getattr(args, "max_steps", 10), None, True)
        elif args.command == "init":
            print("Init command coming soon!")
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
