# Getting Started with Aether

This guide will help you install, understand, and start using Aether — a sovereign, culturally grounded agentic development orchestrator.

## What is Aether?

Aether is a system that helps you plan and execute development work using a combination of:

- A **ReAct-style reasoning loop**
- **Tools** (code search, file reading/writing, memory, etc.)
- **Skills** (reusable patterns for security, reliability, design, releases, etc.)
- Strong **Human-in-the-Loop** controls and guardrails

It is designed to reduce repetitive work while keeping you in control — especially for projects that require high standards of accessibility, security, and cultural safety.

## Installation

### From Source (Recommended)

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
pip install -e .
aether --help
aether skills
aether run "Improve agent context handling and reliability" --max-steps 10
```

## Project Structure

```text
Aether/
├── aether/                 # Core package
│   ├── orchestrator.py
│   ├── guardrails.py
│   ├── memory.py
│   └── tools/
├── skills/                 # Reusable skills
├── docs/                   # Documentation
├── examples/               # Usage examples
├── cli.py                  # Command line interface
├── pyproject.toml
└── README.md
```
