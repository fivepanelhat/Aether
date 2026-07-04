# Using Aether

This guide explains how to use the Aether orchestrator to plan and execute development tasks.

## Quick Start

```python
from aether.orchestrator import AetherOrchestrator

aether = AetherOrchestrator()

# Run a task using the ReAct loop
state = aether.run_react_loop(
    goal="Explore the current codebase and identify security issues in the API routes"
)

print(state.summarize())
```
