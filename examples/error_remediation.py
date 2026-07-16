"""
Example: Error Remediation Workflow

This example demonstrates how Aether can help investigate and propose
fixes for CI failures or application errors.
"""

from aether.orchestrator import AetherOrchestrator


def run_error_remediation_example():
    print("\n" + "=" * 70)
    print("EXAMPLE: Error Remediation Workflow".center(70))
    print("=" * 70 + "\n")

    aether = AetherOrchestrator()

    goal = (
        "A CI pipeline failed with the following error: "
        "'TypeError: Cannot read property of undefined' in the user profile page. "
        "Investigate the likely cause and propose a fix."
    )

    print(f"Goal: {goal}\n")
    print("Running Aether...\n")

    state = aether.run_react_loop(goal=goal, max_steps=7)

    print("\n[Summary]")
    print(state.summarize())

    if hasattr(state, "skill_execution_results"):
        print("\n[Skills Used]")
        for result in state.skill_execution_results:
            print(f"  \u2022 {result.get('skill')}")
            for note in result.get("notes", []):
                print(f"    - {note}")

    print("\n[Important]")
    print("Any code changes or git operations will require your approval.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_error_remediation_example()
