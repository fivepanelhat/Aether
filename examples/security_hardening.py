# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Full Workflow Example: Security Hardening Sprint
Demonstrates tool use + multiple skills working together.
"""

from aether.orchestrator import AetherOrchestrator

def run_security_hardening_sprint():
    print("\n" + "="*70)
    print("EXAMPLE: Security Hardening Sprint".center(70))
    print("="*70 + "\n")

    aether = AetherOrchestrator()

    # Task that should trigger multiple skills
    goal = (
        "Perform a security review of the API routes. "
        "Look for error message leaking, missing authentication, "
        "weak input validation, and any use of raw service role keys."
    )

    state = aether.run_react_loop(goal=goal, max_steps=7)

    print("\n[Final Summary]")
    print(state.summarize())

    print("\n[Skills Triggered]")
    if hasattr(state, "skill_execution_results"):
        for result in state.skill_execution_results:
            print(f"  • {result.get('skill')}")
            for note in result.get("notes", []):
                print(f"    - {note}")
    else:
        print("  (No skills were executed in this run)")

    print("\n[Key Actions Taken]")
    for entry in state.history:
        if any(kw in entry.lower() for kw in ["security", "auth", "validation", "error"]):
            print(f"  {entry}")

    print("\n" + "="*70)
    print("Example completed. Review the output above.".center(70))
    print("="*70 + "\n")


if __name__ == "__main__":
    run_security_hardening_sprint()
