"""
Practical Usage Examples for Aether
"""

from aether.orchestrator import AetherOrchestrator

def example_1_security_audit():
    """Example: Security audit of API routes"""
    aether = AetherOrchestrator()

    state = aether.run_react_loop(
        goal="Audit all API routes for security issues including error leaking and missing auth",
        max_steps=6
    )

    print("\n=== Example 1: Security Audit ===")
    print(state.summarize())


def example_2_component_creation():
    """Example: Creating a UI component"""
    aether = AetherOrchestrator()

    state = aether.run_react_loop(
        goal="Create a new accessible Resource Card component following our design system",
        max_steps=5
    )

    print("\n=== Example 2: Component Creation ===")
    print(state.summarize())


def example_3_with_memory():
    """Example: Using persistent memory across sessions"""
    aether = AetherOrchestrator(memory_path="aether_memory.json")

    state = aether.run_react_loop(
        goal="Find previous decisions related to authentication and security",
        max_steps=4
    )

    print("\n=== Example 3: Using Memory ===")
    print(state.summarize())


if __name__ == "__main__":
    print("Running Aether Usage Examples...\n")

    example_1_security_audit()
    print("\n" + "-"*60 + "\n")

    example_2_component_creation()
    print("\n" + "-"*60 + "\n")

    example_3_with_memory()
