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

## Core Concepts

### Tasks
A task represents a goal you want Aether to work on. When you start a task, Aether will:
- Analyze the goal
- Suggest relevant skills
- Use tools to gather information
- Execute skills when appropriate
- Respect approval gates on high-risk actions

### ReAct Loop
Aether uses a ReAct-style loop (Reason + Act). In each step it will:
- Think about the current state
- Decide whether to use a tool, load a skill, or conclude
- Execute the chosen action
- Record the result
- Repeat until the task is complete or max steps are reached

### Skills
Skills are reusable capabilities that Aether can load and execute. Examples include:
- Security hardening patterns
- Agent reliability improvements
- Build and CI hygiene
- Schema and migration management

Skills are automatically suggested based on the goal, but you can also load them manually.

### Tools
Aether has access to several tools:
- `codebase_search` - Search for code patterns
- `file_reader` - Read file contents
- `memory_query` - Search past task history
- `directory_lister` - Explore project structure
- `file_writer` - Write files (requires approval)

## Common Usage Patterns

### 1. Exploration Task
```python
state = aether.run_react_loop(
 goal="Find all API routes that are missing authentication"
)
```

### 2. Security Hardening Task
```python
state = aether.run_react_loop(
 goal="Audit and fix security issues across all API routes"
)
```

### 3. Feature Implementation Task
```python
state = aether.run_react_loop(
 goal="Create a new accessible Resource Card component following our design system"
)
```

## Approval Gates
Certain actions require human approval before execution:
- Writing files (`file_writer`)
- Git operations (future)
- Deployment actions (future)

When an approval-gated action is triggered, the loop will stop and ask for confirmation.

## Configuration
You can pass a memory path when initializing the orchestrator:
```python
aether = AetherOrchestrator(memory_path="aether_memory.json")
```
This allows Aether to persist memory across sessions.

## Best Practices
- Give clear, specific goals
- Review suggested skills before execution when possible
- Pay attention to approval requests
- Use the `summarize()` method to inspect what Aether has done

## Command-Line Interface

You can also run Aether tasks directly from the command line using the built-in CLI:

```bash
# Run a task
aether run "Your task here"

# Or with more steps
aether run "Fix CSV injection and error leaking issues" --max-steps 10

# List available skills
aether skills
```
