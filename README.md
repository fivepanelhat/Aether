# Aether

**Sovereign Agentic Development System**

Aether is a culturally grounded, extensible agentic development orchestrator. It helps founders and small teams plan and execute development work using tools, reusable skills, and strong human oversight — while staying aligned with Te Tiriti o Waitangi and Te Mana Raraunga principles.

## Quick Start

### 1. Installation

```bash
git clone https://github.com/fivepanelhat/Aether.git
cd Aether
pip install -e .
```

### 2. Verify Installation

```bash
aether --version
aether skills
```

### 3. Run Your First Task

```bash
aether run "Audit the API routes for security issues like error leaking and missing authentication"

# Or run with more reasoning steps:
aether run "Improve conversation history handling in agents" --max-steps 10
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

### Setting Up GitHub Webhooks (Optional but Recommended)

You can configure GitHub to automatically notify Aether when CI fails.

**Steps:**

1. **Start the webhook server**
   ```bash
   python run_webhook.py
   ```

2. **Set your webhook secret** (in your shell or `.env` file)
   ```bash
   export GITHUB_WEBHOOK_SECRET=your-secret-here
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

## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for details.

If you use this software, please provide appropriate credit to the Aether Project.
