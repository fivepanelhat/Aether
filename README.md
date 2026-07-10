# Aether

![Banner](assets/social_preview.png)


**Sovereign Agentic Development System**

Aether is a culturally grounded, extensible agentic development orchestrator. It helps you plan, debug, scaffold, and execute development work using tools and reusable skills — while keeping you in control through strong human oversight.

**Coastal Alpine Tech Limited** - Companion orchestrator for the Kiwi Edge AI Stack.  
**Canonical edge target:** Raspberry Pi 5 **(16GB)** with **Hailo-10H NPU** (40 TOPS). Local LLM via Ollama (`qwen2.5-coder` / Gemma 4 class models).

## Architecture Overview

Aether is the **sovereign agentic development orchestrator** for the stack: ReAct loop over local tools and markdown skills, with HITL gates and optional Ollama (`qwen2.5-coder` / Gemma-class models) on developer or edge hardware.

![Aether architecture — liquid glass overview](assets/architecture_overview.png)

### System map

```mermaid
%%{init: {
  "theme": "dark",
  "themeVariables": {
    "fontSize": "16px",
    "fontFamily": "Inter, ui-sans-serif, system-ui, sans-serif",
    "primaryColor": "#0ea5e9",
    "primaryTextColor": "#f8fafc",
    "primaryBorderColor": "#38bdf8",
    "lineColor": "#67e8f9",
    "secondaryColor": "#1e293b",
    "tertiaryColor": "#0f172a",
    "clusterBkg": "#0b1220cc",
    "clusterBorder": "#38bdf880",
    "titleColor": "#e2e8f0"
  },
  "flowchart": {
    "nodeSpacing": 40,
    "rankSpacing": 48,
    "padding": 20,
    "htmlLabels": true,
    "curve": "basis"
  }
}}%%
flowchart TB

    classDef sense fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
    classDef edge fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
    classDef core fill:#134e4a,stroke:#2dd4bf,stroke-width:2px,color:#f0fdfa
    classDef act fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
    classDef store fill:#1e1b4b,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff
    classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
    classDef app fill:#1e1b4b,stroke:#c4b5fd,stroke-width:2px,color:#eef2ff

    G["Goal / CI signal"] --> ORCH["AetherOrchestrator"]
    ORCH --> LLM["Ollama client<br/>JSON action contract"]
    ORCH --> SK["Skill loader<br/>skills/*/SKILL.md"]
    ORCH --> TL["Tools<br/>read · search · write · memory"]
    ORCH --> GR["Guardrails + threat model<br/>HITL gates"]
    LLM --> DEC["Validated decision"]
    DEC --> GR
    GR -->|approved| TL
    GR -->|halt / approve| HITL["Human approval"]
    TL --> MEM["JSONL memory"]
    SK --> ORCH

    class G,HITL act
    class ORCH,SK,TL core
    class LLM,DEC ai
    class GR store
    class MEM store
```

| Layer | Components | Role |
| :--- | :--- | :--- |
| **Loop** | ReAct + tools | One action per step |
| **Skills** | Markdown packs | Domain procedures |
| **Safety** | Guardrails + HITL | Writes gated by default |
| **LLM** | Ollama local | Offline-capable |

*Full detail: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) · [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)*

## Quick Start

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
pip install -e .

aether --help
aether skills
aether run "Audit the API routes for security issues"
```

- **[Getting Started Guide](docs/GETTING_STARTED.md)**: A complete guide on how to use Aether's ReAct loop and tools.
- **[CLI Reference](docs/CLI_REFERENCE.md)**: A detailed reference of all available CLI commands.

### `aether remediate`

Trigger the error remediation workflow on a specific error or CI failure.

```bash
aether remediate "CI failed on main branch with test error in user.test.ts"
```

## Error Remediation Capabilities

Aether includes a set of skills designed to help with automated debugging and fixing:

- **`error-remediation-orchestrator`** — Coordinates the full process of analyzing errors and proposing fixes.
- **`git-workflow`** — Safely creates branches, commits changes, and opens pull requests (with approval).
- **`ci-failure-parser`** — Extracts useful information from CI failures and GitHub Actions logs.
- **`notification-responder`** — Generates clear status updates and approval requests.

These skills are designed to work together. You can trigger them manually or have them respond to CI failures and GitHub issues.

> **Note**: Git operations and code changes require human approval by default for safety.

## Required Setup for Advanced Features

Some features (especially error remediation and git operations) require additional configuration:

### GitHub Integration (Recommended)

To use the `git-workflow` skill effectively, you should have:

- A GitHub Personal Access Token (classic) with the following scopes:
  - `repo` (Full control of private repositories)
  - `workflow` (Update GitHub Action workflows)

**How to create a token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select the scopes listed above
4. Store the token securely (e.g. in a `.env` file or password manager)

> **Note**: Aether currently expects you to handle git authentication via your local environment (SSH keys or credential manager). Token support can be added later.

### GitHub Webhook Integration (CI Failure Auto-Trigger)

Aether can automatically start remediation when your CI fails.

1. **Start the webhook server**
   ```bash
   python run_webhook.py
   # or
   aether webhook
   # or on a custom port
   aether webhook --host 0.0.0.0 --port 9000
   ```

2. **Set your webhook secret** (required — verification fails closed without it)
   ```bash
   export GITHUB_WEBHOOK_SECRET=your-secure-secret
   # Optional local-dev only bypass (never in production):
   # export AETHER_WEBHOOK_INSECURE=1
   ```

   Install webhook dependencies if needed:
   ```bash
   pip install -e ".[webhook]"
   ```

3. **Expose the server** using [ngrok](https://ngrok.com) or deploy to a server
   ```bash
   ngrok http 8000
   ```

4. **Register the webhook in GitHub**
   - Go to your repo → Settings → Webhooks → Add webhook
   - Payload URL: `https://your-url/webhook/github`
   - Content type: `application/json`
   - Secret: your `GITHUB_WEBHOOK_SECRET` value
   - Events: Select **Workflow runs** and **Check runs**

### Webhook Retry Behavior

When a CI failure is received, Aether will attempt to trigger remediation up to **4 times** using exponential backoff (2s → 4s → 8s → 16s).

If all retry attempts fail, the error is logged but no further automatic action is taken. You can still trigger remediation manually:

```bash
aether run "Investigate CI failure in <repo> on branch <branch>"
```

Retry parameters are configurable via environment variables:

| Variable               | Default | Description                      |
|------------------------|---------|----------------------------------|
| `WEBHOOK_MAX_RETRIES`  | `4`     | Maximum number of retry attempts |
| `WEBHOOK_MIN_WAIT`     | `2`     | Minimum wait between retries (s) |
| `WEBHOOK_MAX_WAIT`     | `30`    | Maximum wait between retries (s) |

### Future Integrations

- Email parsing (for inbox-based remediation)
- Slack / Discord notifications
- GitHub App (for deeper integration without PAT)

## Project Structure

```text
Aether/
├── aether/
│   ├── webhooks/         # GitHub webhook handler (FastAPI)
│   ├── tools/            # Core tools (file_writer, codebase_search, etc.)
│   └── orchestrator.py   # ReAct loop + skill routing
├── skills/               # Reusable skills (add your own here)
├── docs/                 # Documentation
├── examples/             # Usage examples
├── run_webhook.py        # Start the webhook server
├── pyproject.toml        # Packaging configuration
└── README.md
```

## Known Limitations

- Builder capabilities are still early (only the Project Scaffolder exists so far).
- Auto-remediation requires human approval at multiple steps for safety.
- Some advanced features (full auto-remediation, email triggers, etc.) are still in development.

We are actively working on improving generative (builder) capabilities.

## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

If you use this software, please provide appropriate credit to the Aether Project.

---

## Project badges

Status badges for this repository (CI, security, license, and stack metadata):

[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)](LICENSE)  
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)](https://www.python.org/)  
[![Version](https://img.shields.io/badge/version-0.6.3-informational?style=flat-square)](CHANGELOG.md)  
[![Hardware Target](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205%2016GB-C11A5B?style=flat-square&logo=raspberry-pi&logoColor=white)]()  
[![NPU Acceleration](https://img.shields.io/badge/NPU-Hailo--10H%20Accelerated-005A9C?style=flat-square)]()  
[![Sovereignty](https://img.shields.io/badge/Sovereignty-NZ%20Data%20Bound-00247D?style=flat-square)]()  
[![CI](https://github.com/fivepanelhat/Aether/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/Aether/actions/workflows/ci.yml)  
[![Dependabot](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?style=flat-square&logo=dependabot)]()  
[![Sustainability](https://img.shields.io/badge/EECA%20NZ-Carbon%20Tracked-green?style=flat-square)]()
