# Aether

<!-- BEGIN CAT_CONGRUENCE_SNIPPET -->
## Coastal Alpine Tech portfolio

[![Stage](https://img.shields.io/badge/Stage-Pre--seed-8B5CF6)](https://github.com/fivepanelhat/fivepanelhat)
[![Hybrid](https://img.shields.io/badge/Hybrid-Edge%20%2B%20Multi--model-0f766e)](https://github.com/fivepanelhat/fivepanelhat)
[![HITL](https://img.shields.io/badge/HITL-Draft%2FPrepare%20only-dc2626)](./.github/agent-fleet/AGENTS.md)
[![Te Mana Raraunga](https://img.shields.io/badge/Te%20Mana%20Raraunga-Aligned-0f766e)](https://github.com/fivepanelhat/fivepanelhat)

**Part of the [Kiwi Edge AI Stack](https://github.com/fivepanelhat/fivepanelhat)** | Founder OS: [NZ-Start-Up](https://github.com/fivepanelhat/NZ-Start-Up) | Agent policy: [`.github/agent-fleet/`](./.github/agent-fleet/)

> Sovereign hybrid edge AI for NZ farms and founders - local-first + multi-model, Te Mana Raraunga aligned - collaborating with Venture Taranaki, startups.com investors and Kotahitanga Investment Fund (HITL + cultural advisory for formal approaches).

**Agents inform, draft, prepare, monitor, and remind. Humans advise, sign, file, send, and pay.**  
Anti-hallucination policy: [`.github/agent-fleet/anti-hallucination.md`](./.github/agent-fleet/anti-hallucination.md) | Congruence: [`CAT_CONGRUENCE.md`](./CAT_CONGRUENCE.md)
<!-- END CAT_CONGRUENCE_SNIPPET -->


[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://www.python.org)
[![Version](https://img.shields.io/badge/version-0.6.8-blue.svg)](./CHANGELOG.md)

[![Linux](https://img.shields.io/badge/Linux-Ubuntu%2C%20Debian%2C%20Fedora-FCC624?logo=linux&logoColor=black)](https://github.com/fivepanelhat/Aether)
[![Windows](https://img.shields.io/badge/Windows-10%2B-0078D4?logo=windows&logoColor=white)](https://github.com/fivepanelhat/Aether)
[![macOS](https://img.shields.io/badge/macOS-12%2B-000000?logo=apple&logoColor=white)](https://github.com/fivepanelhat/Aether)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-5%20%2816GB%29-C11A5B?logo=raspberry-pi&logoColor=white)](https://github.com/fivepanelhat/Aether)

[![Claude AI](https://img.shields.io/badge/Claude-Anthropic-9C27B0)](https://anthropic.com)
[![Gemini](https://img.shields.io/badge/Gemini-Google-4285F4?logo=google&logoColor=white)](https://gemini.google.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-00A67E)](https://openai.com)
[![Grok](https://img.shields.io/badge/Grok-xAI-000000)](https://x.ai)

[![Hailo NPU](https://img.shields.io/badge/NPU-Hailo--10H-005A9C)](https://github.com/fivepanelhat/Aether)
[![Computer Use](https://img.shields.io/badge/Computer%20Use-Desktop%20Automation-8B5CF6)](./docs/GETTING_STARTED.md)
[![ReAct Loop](https://img.shields.io/badge/ReAct%20Loop-Agentic%20Orchestration-0EA5E9)](./docs/ARCHITECTURE.md)

[![CI Status](https://github.com/fivepanelhat/Aether/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/fivepanelhat/Aether/actions/workflows/ci.yml)
[![Security Status](https://img.shields.io/badge/Dependencies-Monitored-brightgreen?logo=dependabot)](https://github.com/fivepanelhat/Aether/security/dependabot)

![Banner](assets/social_preview.png)

**Sovereign Agentic Development System**

Aether is a culturally grounded, extensible agentic development orchestrator. It helps you plan, debug, scaffold, and execute development work using tools and reusable skills  while keeping you in control through strong human oversight.

**Coastal Alpine Tech Limited**  pre-seed startup, New Plymouth, Taranaki, Aotearoa New Zealand.
**Canonical edge target:** Raspberry Pi 5 **(16GB)** with **Hailo-10H NPU** (40 TOPS). Local LLM via Ollama (`qwen2.5-coder` / Gemma 4 class models).

## Architecture Overview

> **Diagrams:** Architecture images and Mermaid maps describe the **target product architecture** for this pre-seed stack. They are engineering design maps  not claims of large-scale commercial fleet deployment.

Aether is the **sovereign agentic development orchestrator** for the stack: ReAct loop over local tools and markdown skills, with HITL gates and optional Ollama (`qwen2.5-coder` / Gemma-class models) on developer or edge hardware.

![Aether architecture  liquid glass overview](assets/architecture_overview.png)

### System map

```mermaid
%%{init: {
  "theme": "dark",
  "themeVariables": {
    "fontSize": "15px",
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
    "nodeSpacing": 36,
    "rankSpacing": 44,
    "padding": 18,
    "htmlLabels": true,
    "curve": "basis",
    "useMaxWidth": true
  }
}}%%
flowchart TB

    classDef act fill:#422006,stroke:#fbbf24,stroke-width:2px,color:#fffbeb
    classDef core fill:#134e4a,stroke:#2dd4bf,stroke-width:2px,color:#f0fdfa
    classDef ai fill:#3b0764,stroke:#e879f9,stroke-width:2px,color:#fdf4ff
    classDef store fill:#1e1b4b,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff
    classDef host fill:#0c4a6e,stroke:#38bdf8,stroke-width:2px,color:#f0f9ff
    classDef desk fill:#052e16,stroke:#4ade80,stroke-width:2px,color:#f0fdf4
    classDef stack fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#eef2ff

    G["Goal / CI signal"] --> ORCH["AetherOrchestrator<br/>ReAct loop"]
    ORCH --> LLM["Ollama client<br/>JSON action contract"]
    ORCH --> SK["Skill loader<br/>skills/*/SKILL.md"]
    ORCH --> TL["File tools<br/>read | search | write | memory"]
    ORCH --> CU["Computer use hybrid<br/>screenshot | click | type | shell"]
    ORCH --> GR["Guardrails + threat model<br/>HITL gates"]
    LLM --> DEC["Validated decision"]
    DEC --> GR
    GR --> | approved | TL
    GR --> | approved | CU
    GR --> | halt / approve | HITL["Human approval"]
    TL --> MEM["JSONL memory / audit"]
    CU --> MEM
    SK --> ORCH

    subgraph HOSTS["Hybrid hosts  one code path"]
        WIN["Windows 10/11<br/>install.ps1 | pyautogui"]
        LIN["Linux / RPi OS<br/>install.sh | X11/Wayland"]
        MAC["macOS optional"]
    end

    subgraph STACK["Kiwi Edge hybridisation"]
        CORE["Coastal-Alpine-Core skills"]
        WEA["Weaver multi-tenant mesh"]
        CAS["coastal-alpine-stack monorepo"]
    end

    ORCH -.-> HOSTS
    SK -.-> CORE & WEA & CAS
    CU -.-> WIN & LIN

    class G,HITL act
    class ORCH,SK,TL,CU core
    class LLM,DEC ai
    class GR,MEM store
    class WIN,LIN,MAC host
    class CORE,WEA,CAS stack
```

 | Layer | Components | Role |
 | :--- | :--- | :--- |
 | **Loop** | ReAct + tools + computer use | One action per step (files *or* desktop) |
 | **Skills** | Markdown packs + Kiwi Edge skills | Domain procedures + stack architecture |
 | **Safety** | Guardrails + skill HITL | Writes / desktop actuation gated by default |
 | **LLM** | Ollama local (text + vision) | Offline-capable on Windows, Linux, RPi |
 | **Hosts** | `install.ps1` | `install.sh` | Same package; dual-platform installers |
 | **Hybrid stack** | Core | Weaver | coastal-alpine-stack | Companion for sovereign edge development |

*Full detail: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | [docs/GETTING_STARTED.md](./docs/GETTING_STARTED.md)*

## Quick Start

### One-line install (recommended)

<details open>
<summary><strong>ðŸ§ Linux / macOS</strong></summary>

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh | bash
aether doctor
```

</details>

<details>
<summary><strong>ðŸªŸ Windows (PowerShell)</strong></summary>

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 | iex
aether doctor
```

> **Note:** If script execution is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

</details>

### From a clone

<details open>
<summary><strong>ðŸ§ Linux / macOS</strong></summary>

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[computer]"   # or: pip install -e .  for CLI only
aether init
aether --help
aether skills
aether run "Audit the API routes for security issues"
```

</details>

<details>
<summary><strong>ðŸªŸ Windows (PowerShell)</strong></summary>

```powershell
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[computer]"   # or: pip install -e .  for CLI only
aether init
aether --help
aether skills
aether run "Audit the API routes for security issues"
```

</details>

**Prerequisites (both platforms):** Python 3.10+, Git, [Ollama](https://ollama.com) for local models. On Linux desktop control also needs a display server (X11/Wayland) and often `python3-tk` / `scrot` depending on distro.

Skills ship inside the package (`aether/bundled_skills`) so `pip install` works without a git checkout. `aether init` copies them to the user/project locations. Discovery order: `AETHER_SKILLS_DIR` â†' `./skills` â†' `~/.aether/skills` â†' packaged skills.

All file tools (read/write/search/list) are sandboxed to the process working directory (allowed root). Paths are handled portably on **Linux and Windows** (mixed separators, case-insensitive roots on Windows, UTF-8 console/logs).

- **[Getting Started Guide](docs/GETTING_STARTED.md)**: A complete guide on how to use Aether's ReAct loop and tools.
- **[CLI Reference](docs/CLI_REFERENCE.md)**: A detailed reference of all available CLI commands.

### `aether remediate`

Trigger the error remediation workflow on a specific error or CI failure.

```bash
aether remediate "CI failed on main branch with test error in user.test.ts"
```

## Computer Use  Edge AI that operates your desktop

Aether now hybridises **sovereign edge AI** with **computer use**: a local
(Ollama) vision model looks at screenshots and drives the real mouse, keyboard,
and shell to accomplish goals  entirely on-device. No screenshots or keystrokes
leave the machine. Works on **Windows and Linux** (and macOS) from one code path.

### Download & install (terminal, cross-platform)

**Linux / macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.sh | bash
```

**Windows (PowerShell)**

```powershell
irm https://raw.githubusercontent.com/fivepanelhat/Aether/main/install.ps1 | iex
```

Or from a clone, install the desktop extras alongside the base package:

```bash
pip install -e ".[computer]"     # adds pyautogui + Pillow
aether doctor                    # verify Ollama + display + backend
```

The installers create an isolated virtualenv, expose the `aether` command on your
PATH, install the bundled skills, and check for the local [Ollama](https://ollama.com)
runtime. Pull a vision model once:

```bash
ollama pull qwen2.5-vl:7b        # vision model for the agentic loop
ollama pull qwen2.5-coder:7b     # text model for `aether run`
```

### Agentic desktop control

```bash
# Vision loop: Aether observes the screen and acts to reach the goal.
aether computer run "Open the calculator and compute 12 * 9"
aether computer run "Rename the selected file to report_final.txt" --max-steps 15

# Authorize actuation without per-step prompts (batch / trusted contexts):
aether computer run "Tidy my downloads folder" --auto-approve

# Rehearse without touching the mouse/keyboard:
aether computer run "..." --dry-run
```

By default every actuating step (click, type, key, scroll, shell) pauses for
**human approval** on a TTY, routed through the same guardrails/HITL layer that
gates Aether's file writes. `screenshot` and `screen_info` are read-only and
never gated.

### Direct control (deterministic, no model needed)

```bash
aether computer shot screen.png            # capture a screenshot
aether computer info                       # screen size + cursor position
aether computer click 640 480 --button left
aether computer move 200 200
aether computer type "kia ora"
aether computer key ctrl+s
aether computer scroll -3
```

### Compatibility with the existing stack

The computer-use tools register into the **same ReAct orchestrator, guardrails,
threat model, and JSONL memory/audit trail** as the rest of Aether, so
`aether run` can also mix desktop actuation with file/search/skill steps. Prompt
goals are screened for injection before any action runs, coordinates are clamped
to the real screen, and the PyAutoGUI fail-safe (fling the cursor to a corner to
abort) stays on. When there is no display or the extras aren't installed, the
tools degrade gracefully with an actionable message instead of crashing.

Environment switches: `AETHER_COMPUTER_DRY_RUN=1` rehearses without actuating;
the vision model/host are overridable with `--model` / `--base-url`.

## Skills

Skills are markdown packs under `skills/*/SKILL.md`, auto-loaded at runtime. Full catalogue: **[docs/SKILLS_CATALOG.md](./docs/SKILLS_CATALOG.md)**.

```bash
python -m aether.cli skills
# or, after install:
aether skills
```

### Architecture & sovereignty (Kiwi Edge companion)

 | Skill | Role |
 | ----- | ---- |
 | **`kiwi-edge-architecture`** | System map: field â†' MQTT â†' Core â†' Weaver â†' portals â†' Ollama/Hailo on **RPi 5 16GB + Hailo-10H** |
 | **`security-notifications-triage`** | Dependabot / GHSA / CodeQL / audit response (HITL for high-impact) |
 | **`te-mana-raraunga-sovereignty`** | **Te Mana Raraunga 2018** data-sovereignty constraints |

### Error remediation

 | Skill | Role |
 | ----- | ---- |
 | **`error-remediation-orchestrator`** | Analyze failures and propose/apply fixes (HITL) |
 | **`git-workflow`** | Branch, commit, push, PR (HITL) |
 | **`ci-failure-parser`** | Structure CI / Actions logs |
 | **`notification-responder`** | Status updates and approval requests |

### Security auditors

`security-route-audit`, `security-auth-guard`, `error-message-sanitization`, `service-role-key-protection`, `strict-zod-schema-enforcement`, `release-preflight`, plus CI hygiene skills.

Trigger manually or via GitHub webhook remediation:

```bash
aether run "Apply kiwi-edge-architecture and Te Mana Raraunga checks to this Core PR"
aether remediate "CI failed on main with test error in user.test.ts"
```

> **Note**: Git operations, code writes, and high-impact security changes require human approval by default.

## Required Setup for Advanced Features

Some features (especially error remediation and git operations) require additional configuration:

### GitHub Integration (Recommended)

To use the `git-workflow` skill effectively, you should have:

- A GitHub Personal Access Token (classic) with the following scopes:
  - `repo` (Full control of private repositories)
  - `workflow` (Update GitHub Action workflows)

**How to create a token:**
1. Go to GitHub â†' Settings â†' Developer settings â†' Personal access tokens â†' Tokens (classic)
2. Generate new token
3. Select the scopes listed above
4. Store the token securely (e.g. in a `.env` file or password manager)

> **Note**: Aether currently expects you to handle git authentication via your local environment (SSH keys or credential manager). Token support can be added later.

### GitHub Webhook Integration (CI Failure Auto-Trigger)

Aether can start investigation when your CI fails. **Default is propose-only** (read tools + plan; high-risk writes halt for HITL). Opt in to unattended writes with `AETHER_WEBHOOK_AUTO_REMEDIATE=1`.

1. **Start the webhook server**
   ```bash
   python run_webhook.py
   # or
   aether webhook
   # or on a custom port
   aether webhook --host 0.0.0.0 --port 9000
   ```

2. **Set your webhook secret** (required  verification fails closed without it)
   ```bash
   export GITHUB_WEBHOOK_SECRET=your-secure-secret
   # Optional local-dev only bypass (never in production):
   # export AETHER_WEBHOOK_INSECURE=1
   # Optional: authorize high-risk tool actions from webhooks (default off):
   # export AETHER_WEBHOOK_AUTO_REMEDIATE=1
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
   - Go to your repo â†' Settings â†' Webhooks â†' Add webhook
   - Payload URL: `https://your-url/webhook/github`
   - Content type: `application/json`
   - Secret: your `GITHUB_WEBHOOK_SECRET` value
   - Events: Select **Workflow runs** and **Check runs**

### Webhook Retry Behavior

When a CI failure is received, Aether will attempt to trigger remediation up to **4 times** using exponential backoff (2s â†' 4s â†' 8s â†' 16s).

If all retry attempts fail, the error is logged but no further automatic action is taken. You can still trigger remediation manually:

```bash
aether run "Investigate CI failure in <repo> on branch <branch>"
```

Retry parameters are configurable via environment variables:

 | Variable | Default | Description |
 | ------------------------ | --------- | ---------------------------------- |
 | `WEBHOOK_MAX_RETRIES` | `4` | Maximum number of retry attempts |
 | `WEBHOOK_MIN_WAIT` | `2` | Minimum wait between retries (s) |
 | `WEBHOOK_MAX_WAIT` | `30` | Maximum wait between retries (s) |

### Future Integrations

- Email parsing (for inbox-based remediation)
- Slack / Discord notifications
- GitHub App (for deeper integration without PAT)

## Project Structure

```text
Aether/
â"œâ"€â"€ aether/
â"‚   â"œâ"€â"€ webhooks/         # GitHub webhook handler (FastAPI)
â"‚   â"œâ"€â"€ tools/            # Core tools (file_writer, codebase_search, etc.)
â"‚   â""â"€â"€ orchestrator.py   # ReAct loop + skill routing
â"œâ"€â"€ skills/               # Reusable skills (add your own here)
â"œâ"€â"€ docs/                 # Documentation
â"œâ"€â"€ examples/             # Usage examples
â"œâ"€â"€ run_webhook.py        # Start the webhook server
â"œâ"€â"€ pyproject.toml        # Packaging configuration
â""â"€â"€ README.md
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

**Built with focus on data sovereignty and edge intelligence.**
**Coastal Alpine Tech Limited  New Plymouth, Taranaki, New Zealand.**
