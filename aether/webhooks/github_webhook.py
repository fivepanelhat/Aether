"""
GitHub Webhook Handler for Aether

Receives webhooks from GitHub and triggers remediation when CI fails.
"""

import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from aether.orchestrator import AetherOrchestrator
import logging

logger = logging.getLogger("AetherGitHubWebhook")

app = FastAPI(title="Aether GitHub Webhook Handler")

# Load secret from environment
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature."""
    if not GITHUB_WEBHOOK_SECRET:
        logger.warning("GITHUB_WEBHOOK_SECRET not set. Skipping signature verification.")
        return True

    mac = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event")
    data = await request.json()

    logger.info(f"Received GitHub event: {event}")

    # Handle CI failures
    if event in ["workflow_run", "check_run"]:
        conclusion = data.get("workflow_run", {}).get("conclusion") or data.get("check_run", {}).get("conclusion")

        if conclusion == "failure":
            repo = data.get("repository", {}).get("full_name")
            branch = data.get("workflow_run", {}).get("head_branch") or data.get("check_run", {}).get("head_branch")
            commit_sha = data.get("workflow_run", {}).get("head_sha") or data.get("check_run", {}).get("head_sha")

            logger.info(f"CI failure detected in {repo} on branch {branch}")

            # Trigger remediation in background
            background_tasks.add_task(
                trigger_remediation,
                repo=repo,
                branch=branch,
                commit_sha=commit_sha,
                event_data=data
            )

    return {"status": "received"}


def trigger_remediation(repo: str, branch: str, commit_sha: str, event_data: dict):
    """
    Trigger the error remediation orchestrator.
    This runs in the background.
    """
    try:
        aether = AetherOrchestrator()

        goal = (
            f"CI failed in repository {repo} on branch {branch} (commit {commit_sha}). "
            f"Please investigate the failure and propose a fix."
        )

        logger.info(f"Triggering remediation for: {goal}")

        state = aether.run_react_loop(
            goal=goal,
            max_steps=8
        )

        logger.info(f"Remediation completed. Summary: {state.summarize()}")

    except Exception as e:
        logger.error(f"Error during remediation trigger: {e}")
