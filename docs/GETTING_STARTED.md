# Getting Started with Aether

This guide will help you install and start using Aether.

## What is Aether?

Aether is an agentic development system that can help you with tasks such as:

- Auditing code for security and quality issues
- Debugging and proposing fixes for CI failures
- Running structured development workflows using reusable skills
- Safely applying code changes through git

## Installation (Windows + Linux)

Aether is dual-platform: **Windows 10/11**, **Linux** (including RPi OS), and macOS. Hybrid extras add **computer use** (desktop control) on the same install path.

### One-line installers

**Linux / macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh | bash
aether doctor
```

**Windows (PowerShell)**

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 | iex
aether doctor
```

### From a clone

<details open>
<summary><strong>🐧 Linux / macOS</strong></summary>

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[computer]"   # or: pip install -e .
aether init
```

</details>

<details>
<summary><strong>🪟 Windows (PowerShell)</strong></summary>

```powershell
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[computer]"   # or: pip install -e .
aether init
```

</details>

**Prerequisites:** Python 3.10+, Git, [Ollama](https://ollama.com). Linux computer-use may need a display (X11/Wayland) and distro packages such as `python3-tk`.

## Verify

```bash
aether --version
aether skills
aether doctor
```

## Running Tasks

```bash
# Security audit
aether run "Audit the API routes for security issues"

# With more reasoning steps
aether run "Improve agent context handling and reliability" --max-steps 10

# Trigger auto-remediation
aether run "Fix failing tests on main branch" --auto-remediate

# Remediate a CI failure
aether remediate "CI failed on main with test error in user.test.ts"
```

## Project Structure

```text
Aether/
├── aether/
│   ├── orchestrator.py     # ReAct loop + skill routing
│   ├── guardrails.py       # Human-in-the-loop controls
│   ├── memory.py           # Persistent memory
│   ├── tools/              # Core tools (file_writer, codebase_search, etc.)
│   └── webhooks/           # GitHub webhook handler (FastAPI)
├── skills/                 # Reusable skills (add your own here)
├── docs/                   # Documentation
├── examples/               # Usage examples
├── run_webhook.py          # Start the webhook server
├── pyproject.toml
└── README.md
```

## Skills

Skills are reusable instruction sets that tell Aether how to handle specific tasks.

```bash
aether skills   # list all loaded skills
```

Each skill lives in `skills/<skill-name>/SKILL.md`. To create a new skill, add a folder with a `SKILL.md` file using the standard YAML frontmatter format.

## Webhook Integration (Optional)

To automatically trigger remediation on CI failures:

```bash
# Install optional webhook dependencies
pip install aether[webhook]

# Start the server
aether webhook
# or
python run_webhook.py
```

Then register `https://your-url/webhook/github` in your GitHub repo settings.

> **Note**: Set `GITHUB_WEBHOOK_SECRET` in your environment for security.

## Key Principles

Aether is built on the following principles:

- **Sovereignty**: You stay in control. High-risk actions require explicit approval.
- **Te Tiriti alignment**: Designed with respect for Te Tiriti o Waitangi and Te Mana Raraunga.
- **Transparency**: All actions are logged and summarized.
- **Extensibility**: Add new skills to extend what Aether can do.

## Try the Examples

After installing Aether, you can explore some practical examples:

```bash
python examples/project_scaffolding_example.py
python examples/error_remediation_example.py
```
