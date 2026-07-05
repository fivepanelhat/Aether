"""
GitHub Webhook Handler for Aether (with Retry Logic)
"""

import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

from aether.orchestrator import AetherOrchestrator

logger = logging.getLogger("AetherGitHubWebhook")

app = FastAPI(title="Aether GitHub Webhook Handler")

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    if not GITHUB_WEBHOOK_SECRET:
        logger.warning("GITHUB_WEBHOOK_SECRET not set. Skipping signature verification.")
        return True

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)


def _extract_failure_info(data: dict, event: str) -> dict | None:
    """Extract relevant failure information from GitHub events."""
    if event == "workflow_run":
        wr = data.get("workflow_run", {})
        if wr.get("conclusion") == "failure":
            return {
                "repo": data.get("repository", {}).get("full_name"),
                "branch": wr.get("head_branch"),
                "commit_sha": wr.get("head_sha"),
                "workflow_name": wr.get("name"),
                "html_url": wr.get("html_url"),
            }
    elif event == "check_run":
        cr = data.get("check_run", {})
        if cr.get("conclusion") == "failure":
            return {
                "repo": data.get("repository", {}).get("full_name"),
                "branch": cr.get("head_branch"),
                "commit_sha": cr.get("head_sha"),
                "check_name": cr.get("name"),
                "html_url": cr.get("html_url"),
            }
    return None


@retry(
    stop=stop_after_attempt(4),                          # Retry up to 4 times
    wait=wait_exponential(multiplier=1, min=2, max=30),  # 2s, 4s, 8s, 16s...
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def trigger_ci_remediation_with_retry(failure_info: dict):
    """Retry wrapper around the remediation trigger."""
    try:
        aether = AetherOrchestrator()

        goal = (
            f"CI failed in {failure_info['repo']} on branch {failure_info['branch']} "
            f"(commit {failure_info.get('commit_sha', 'unknown')}). "
            f"Please investigate and propose a fix."
        )

        logger.info(f"Triggering remediation (attempt) for: {goal}")

        state = aether.run_react_loop(goal=goal, max_steps=8)
        logger.info(f"Remediation completed successfully.")

    except Exception as e:
        logger.warning(f"Remediation attempt failed: {e}")
        raise  # Let tenacity handle the retry


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")
    data = await request.json()

    failure_info = _extract_failure_info(data, event)

    if failure_info:
        logger.info(f"CI failure detected → {failure_info['repo']}@{failure_info['branch']}")

        # Run remediation with retry logic in the background
        background_tasks.add_task(trigger_ci_remediation_with_retry, failure_info)

    return {"status": "received"}
