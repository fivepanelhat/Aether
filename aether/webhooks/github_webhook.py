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
# Opt-in only: allow unsigned webhooks for local dev. Never enable in production.
ALLOW_INSECURE = os.getenv("AETHER_WEBHOOK_INSECURE", "").lower() in ("1", "true", "yes")
# Opt-in only: authorize high-risk tool actions (e.g. file_writer) from webhooks.
# Default is propose-only (investigate + plan; halt on HITL actions).
AUTO_REMEDIATE = os.getenv("AETHER_WEBHOOK_AUTO_REMEDIATE", "").lower() in ("1", "true", "yes")

# Retry configuration — override via environment variables
MAX_RETRIES = int(os.getenv("WEBHOOK_MAX_RETRIES", "4"))
MIN_WAIT = int(os.getenv("WEBHOOK_MIN_WAIT", "2"))
MAX_WAIT = int(os.getenv("WEBHOOK_MAX_WAIT", "30"))


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Validate GitHub X-Hub-Signature-256.

    Fails closed when GITHUB_WEBHOOK_SECRET is unset, unless
    AETHER_WEBHOOK_INSECURE=1 is explicitly set for local development.
    """
    if not GITHUB_WEBHOOK_SECRET:
        if ALLOW_INSECURE:
            logger.warning(
                "GITHUB_WEBHOOK_SECRET not set and AETHER_WEBHOOK_INSECURE=1 — "
                "skipping signature verification (dev only)."
            )
            return True
        logger.error(
            "GITHUB_WEBHOOK_SECRET not set. Refusing webhook. "
            "Set the secret, or AETHER_WEBHOOK_INSECURE=1 for local dev only."
        )
        return False

    if not signature:
        return False

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
                "branch": cr.get("check_suite", {}).get("head_branch") or cr.get("head_branch"),
                "commit_sha": cr.get("head_sha"),
                "check_name": cr.get("name"),
                "html_url": cr.get("html_url"),
            }
    return None


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=MIN_WAIT, max=MAX_WAIT),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def trigger_ci_remediation_with_retry(failure_info: dict):
    """Retry wrapper around the remediation trigger.

    Default: propose-only (auto_remediate=False). High-risk actions halt with
    pending approval. Set AETHER_WEBHOOK_AUTO_REMEDIATE=1 only when writes are
    intentionally authorized for unattended remediation.
    """
    try:
        aether = AetherOrchestrator()

        if AUTO_REMEDIATE:
            goal = (
                f"CI failed in {failure_info.get('repo', 'unknown')} on branch "
                f"{failure_info.get('branch', 'unknown')} "
                f"(commit {failure_info.get('commit_sha', 'unknown')}). "
                f"Investigate and apply a minimal fix if safe. URL: "
                f"{failure_info.get('html_url', 'n/a')}"
            )
        else:
            goal = (
                f"CI failed in {failure_info.get('repo', 'unknown')} on branch "
                f"{failure_info.get('branch', 'unknown')} "
                f"(commit {failure_info.get('commit_sha', 'unknown')}). "
                f"Investigate with read-only tools and propose a concrete fix plan. "
                f"Do not write files or mutate git state. URL: "
                f"{failure_info.get('html_url', 'n/a')}"
            )

        logger.info(
            f"Triggering remediation (auto_remediate={AUTO_REMEDIATE}) for: {goal}"
        )

        aether.run_react_loop(
            goal=goal,
            max_steps=8,
            auto_remediate=AUTO_REMEDIATE,
        )
        logger.info("Remediation completed successfully.")

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
        logger.info(f"CI failure detected → {failure_info.get('repo')}@{failure_info.get('branch')}")
        background_tasks.add_task(trigger_ci_remediation_with_retry, failure_info)

    return {"status": "received"}
