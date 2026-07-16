"""
Example: Using the Project Scaffolder Skill

This example shows how Aether can help bootstrap a new project
or feature with a consistent structure.
"""

from aether.orchestrator import AetherOrchestrator


def run_project_scaffolding_example():
 print("\n" + "=" * 70)
 print("EXAMPLE: Project Scaffolding".center(70))
 print("=" * 70 + "\n")

 aether = AetherOrchestrator()

 goal = (
 "Scaffold a new Next.js feature for a resource directory page. "
 "Include proper folder structure, a basic page, and reusable components "
 "following our design system conventions."
 )

 print(f"Goal: {goal}\n")
 print("Running Aether...\n")

 state = aether.run_react_loop(goal=goal, max_steps=6)

 print("\n[Summary]")
 print(state.summarize())

 if hasattr(state, "skill_execution_results"):
 print("\n[Skills Used]")
 for result in state.skill_execution_results:
 print(f" \u2022 {result.get('skill')}")
 for note in result.get("notes", []):
 print(f" - {note}")

 print("\n[Key Actions]")
 for entry in state.history[-6:]:
 print(f" {entry}")

 print("\n" + "=" * 70)
 print("Note: File writing requires human approval.".center(70))
 print("=" * 70 + "\n")


if __name__ == "__main__":
 run_project_scaffolding_example()
