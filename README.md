# Aether

**Sovereign Agentic Development System**

Aether is a culturally grounded, extensible agentic development orchestrator designed to help founders and small teams build high-quality software while maintaining strong human oversight and alignment with Te Tiriti o Waitangi and Te Mana Raraunga principles.

## Quick Start

### Installation

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
pip install -e .
```

### Usage

```bash
# See available skills
aether skills

# Run a task
aether run "Audit the API routes for security issues and missing validation"

# Run with more reasoning steps
aether run "Improve conversation history handling in agents" --max-steps 10
```

- **[Getting Started Guide](docs/GETTING_STARTED.md)**: A complete guide on how to use Aether's ReAct loop and tools.
- **[CLI Reference](docs/CLI_REFERENCE.md)**: A detailed reference of all available CLI commands.

## Project Structure

```text
Aether/
├── aether/
│   ├── __init__.py
│   └── orchestrator.py
├── docs/
│   ├── AETHER_SKILL_FORMAT.md
│   ├── AETHER_VISION.md
│   ├── ROADMAP.md
│   └── COMPLIANCE.md
├── skills/
├── examples/
├── tests/
├── README.md
├── COMPLIANCE.md
├── pyproject.toml
└── .gitignore
```

## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

If you use this software, please provide appropriate credit to the Aether Project.
