# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Practical Usage Examples for Aether
Demonstrates tool usage, skill execution, and result inspection.
"""

from aether.orchestrator import AetherOrchestrator


def run_and_show_results(goal: str, max_steps: int = 6):
    """Helper to run a task and display results nicely."""
    aether = AetherOrchestrator()
    state = aether.run_react_loop(goal=goal, max_steps=max_steps)

    print("\n" + "="*70)
    print(f"GOAL: {goal}")
    print("="*70)

    print("\n[Final Summary]")
    print(state.summarize())

    if hasattr(state, "skill_execution_results") and state.skill_execution_results:
        print("\n[Skill Execution Results]")
        for res in state.skill_execution_results:
            print(f"  Skill: {res.get('skill')}")
            for note in res.get("notes", []):
                print(f"    - {note}")

    print("\n[Recent History]")
    for entry in state.history[-8:]:
        print(f"  {entry}")

    print("\n" + "="*70 + "\n")
    return state


def example_security_audit():
    run_and_show_results(
        goal="Audit API routes for error leaking, missing auth, and weak validation",
        max_steps=6
    )


def example_agent_reliability():
    run_and_show_results(
        goal="Improve agent context handling and reduce dropped conversation history",
        max_steps=5
    )


def example_build_and_schema():
    run_and_show_results(
        goal="Check for build issues and schema drift in the database layer",
        max_steps=5
    )


if __name__ == "__main__":
    print("Running Aether Examples...\n")

    example_security_audit()
    example_agent_reliability()
    example_build_and_schema()
