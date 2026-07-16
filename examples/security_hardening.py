# Copyright 2026 Aether Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
 print(f" - {result.get('skill')}")
 for note in result.get("notes", []):
 print(f" - {note}")
 else:
 print(" (No skills were executed in this run)")

 print("\n[Key Actions Taken]")
 for entry in state.history:
 if any(kw in entry.lower() for kw in ["security", "auth", "validation", "error"]):
 print(f" {entry}")

 print("\n" + "="*70)
 print("Example completed. Review the output above.".center(70))
 print("="*70 + "\n")


if __name__ == "__main__":
 run_security_hardening_sprint()
