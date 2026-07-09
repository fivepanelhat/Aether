# Aether

**Sovereign Agentic Development System**

Aether is a culturally grounded, extensible agentic development orchestrator. It helps you plan, debug, scaffold, and execute development work using tools and reusable skills - while keeping you in control through strong human oversight.

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

1. **Install the webhook extras and start the server**
   ```bash
   pip install -e ".[webhook]"
   python run_webhook.py
   # or
   aether webhook
   # or on a custom port
   aether webhook --host 0.0.0.0 --port 9000
   ```

2. **Set your webhook secret** (in your shell or `.env` file)
   ```bash
   export GITHUB_WEBHOOK_SECRET=your-secure-secret
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
