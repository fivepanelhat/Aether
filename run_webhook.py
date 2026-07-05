"""
Run the Aether GitHub Webhook server.
Usage: python run_webhook.py
"""

import uvicorn
from aether.webhooks.github_webhook import app

if __name__ == "__main__":
    print("Starting Aether GitHub Webhook server on http://0.0.0.0:8000")
    print("Set GITHUB_WEBHOOK_SECRET in your environment for security.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
