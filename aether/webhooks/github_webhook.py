"""
GitHub Webhook Handler for Aether (Production Grade)

Handles CI failures from GitHub and triggers the remediation workflow.
"""

import os
import hmac
import hashlib
import json
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from typing import Optional
import logging

from aether.orchestrator import AetherOrchestrator

logger = logging.getLogger("AetherGitHubWebhook")

app = FastAPI(title="Aether GitHub Webhook Handler", version="0.1.0")

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature for security."""
    if not GITHUB_WEBHOOK_SECRET:
        logger.warning("GITHUB_WEBHOOK_SECRET not set — skipping signature verification (not recommended for production).")
        return True

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode("utf-8"), msg=payload, digestmod=hashlib.sha256)
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)


def _extract_failure_info(data: dict, event: str) -> Optional[dict]:
    """Extract useful information from CI failure events."""
    if event == "workflow_run":
        workflow_run = data.get("workflow_run", {})
        if workflow_run.get("conclusion") == "failure":
            return {
                "repo": data.get("repository", {}).get("full_name"),
                "branch": workflow_run.get("head_branch"),
                "commit_sha": workflow_run.get("head_sha"),
                "workflow_name": workflow_run.get("name"),
                "run_id": workflow_run.get("id"),
                "html_url": workflow_run.get("html_url"),
            }

    elif event == "check_run":
        check_run = data.get("check_run", {})
        if check_run.get("conclusion") == "failure":
            return {
                "repo": data.get("repository", {}).get("full_name"),
                "branch": check_run.get("head_branch"),
                "commit_sha": check_run.get("head_sha"),
                "check_name": check_run.get("name"),
                "html_url": check_run.get("html_url"),
            }

    return None


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    event = request.headers.get("X-GitHub-Event", "")
    data = await request.json()

    failure_info = _extract_failure_info(data, event)

    if failure_info:
        logger.info(f"CI failure detected in {failure_info['repo']} on branch {failure_info['branch']}")
        
        background_tasks.add_task(
            trigger_ci_remediation,
            failure_info=failure_info
        )

    return {"status": "received", "event": event}


def trigger_ci_remediation(failure_info: dict):
    """Background task to trigger remediation."""
    try:
        aether = AetherOrchestrator()

        goal = (
            f"CI failed in {failure_info['repo']} on branch {failure_info['branch']} "
            f"(commit {failure_info.get('commit_sha', 'unknown')}). "
            f"Workflow/Check: {failure_info.get('workflow_name') or failure_info.get('check_name')}. "
            f"Please investigate and propose a fix. Link: {failure_info.get('html_url', '')}"
        )

        logger.info(f"Triggering remediation for CI failure: {goal}")

        state = aether.run_react_loop(goal=goal, max_steps=8)
        logger.info(f"Remediation completed. Summary: {state.summarize()}")

    except Exception as e:
        logger.error(f"Error during CI remediation trigger: {e}", exc_info=True)
