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
Aether CLI - Professional Command Line Interface
"""

import argparse
import sys
from aether.orchestrator import AetherOrchestrator

__version__ = "0.5.0"


def print_header(text: str):
    print("\n" + "=" * 72)
    print(text.center(72))
    print("=" * 72)


def run_task(goal: str, max_steps: int = 8, memory_path: str = None, auto_remediate: bool = False):
    if not goal or goal.strip() == "":
        print("Error: Please provide a goal.\nExample: aether run \"Audit the API routes for security issues\"")
        sys.exit(1)

    print_header("AETHER")

    print(f"Goal: {goal}")
    print(f"Max Steps: {max_steps}")
    print(f"Auto-Remediate: {auto_remediate}")
    print("-" * 72)

    try:
        aether = AetherOrchestrator(memory_path=memory_path)
        state = aether.run_react_loop(goal=goal, max_steps=max_steps, auto_remediate=auto_remediate)

        print("\n[Summary]")
        print(state.summarize())

        if hasattr(state, "skill_execution_results") and state.skill_execution_results:
            print("\n[Skills Used]")
            for result in state.skill_execution_results:
                print(f"  \u2022 {result.get('skill')}")

        print("\n[Recent Activity]")
        for entry in state.history[-8:]:
            print(f"  {entry}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Error] {e}")
        sys.exit(1)

    print("\n" + "=" * 72)
    print("Task completed.")
    print("=" * 72 + "\n")


def list_skills():
    try:
        aether = AetherOrchestrator()
        print_header("AVAILABLE SKILLS")

        skills = aether.get_available_skills()

        if not skills:
            print("No skills found.")
            print("Create skills in the 'skills/' directory to extend Aether's capabilities.")
            return

        for name in skills:
            info = aether.get_skill_info(name) or {}
            desc = info.get("description", "No description available")
            print(f"  {name}")
            try:
                print(f"    {desc}\n")
            except UnicodeEncodeError:
                clean_desc = desc.encode("ascii", "ignore").decode("ascii")
                print(f"    {clean_desc}\n")

    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)


def start_webhook_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the GitHub webhook server."""
    try:
        import uvicorn
        from aether.webhooks.github_webhook import app

        print(f"\nStarting Aether GitHub Webhook server on http://{host}:{port}")
        print("Set GITHUB_WEBHOOK_SECRET environment variable for security.\n")

        uvicorn.run(app, host=host, port=port)
    except ImportError:
        print("Error: uvicorn is not installed. Run: pip install uvicorn fastapi")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Aether - Sovereign Agentic Development System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aether run "Audit the API routes for security issues"
  aether run "Improve context handling in agents" --max-steps 10
  aether remediate "CI failed on main with test error in user.test.ts"
  aether skills
  aether webhook --port 9000
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show Aether version"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === Run Command ===
    run_parser = subparsers.add_parser(
        "run",
        help="Run a task using the ReAct reasoning loop"
    )
    run_parser.add_argument(
        "goal",
        type=str,
        help="The goal or task you want Aether to work on"
    )
    run_parser.add_argument(
        "--max-steps",
        type=int,
        default=8,
        help="Maximum number of reasoning steps (default: 8)"
    )
    run_parser.add_argument(
        "--memory",
        type=str,
        default=None,
        help="Path to persist memory across runs"
    )
    run_parser.add_argument(
        "--auto-remediate",
        action="store_true",
        help="Authorize Aether to automatically fix issues, create branches, and run tests"
    )

    # === Skills Command ===
    subparsers.add_parser(
        "skills",
        help="List all available skills"
    )

    # === Init Command ===
    subparsers.add_parser(
        "init",
        help="Initialize Aether in the current project (coming soon)"
    )

    # === Remediate Command ===
    remediate_parser = subparsers.add_parser(
        "remediate",
        help="Trigger the error remediation workflow on a CI failure or error"
    )
    remediate_parser.add_argument(
        "error",
        type=str,
        help="The error or CI failure to remediate"
    )

    # === Webhook Command ===
    webhook_parser = subparsers.add_parser(
        "webhook",
        help="Start the GitHub webhook server"
    )
    webhook_parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    webhook_parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")

    try:
        args = parser.parse_args()

        if not hasattr(args, "command") or not args.command:
            parser.print_help()
            sys.exit(1)

        if args.command == "run":
            run_task(args.goal, args.max_steps, args.memory, getattr(args, "auto_remediate", False))
        elif args.command == "skills":
            list_skills()
        elif args.command == "init":
            print("Init command coming soon!")
        elif args.command == "remediate":
            if not getattr(args, "error", "") or args.error.strip() == "":
                print("Error: Please provide an error.\nExample: aether remediate \"CI failed on main branch\"")
                sys.exit(1)
            goal = f"Remediate the following error using error-remediation-orchestrator: {args.error}"
            run_task(goal, max_steps=10, auto_remediate=True)
        elif args.command == "webhook":
            start_webhook_server(
                host=getattr(args, "host", "0.0.0.0"),
                port=getattr(args, "port", 8000)
            )
        else:
            parser.print_help()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
