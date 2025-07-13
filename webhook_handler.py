# 处理 GitHub Webhook

from flask import request, abort
import hmac, hashlib, json
from pr_processor import handle_pull_request
from config import WEBHOOK_SECRET

def github_webhook():
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = request.data

    mac = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256)
    expected_sig = "sha256=" + mac.hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        abort(400, "Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")
    payload = json.loads(body)
    action = payload.get("action", "")

    if event == "pull_request" and action in ("opened", "synchronize", "ready_for_review"):
        pr = payload["pull_request"]
        repo_info = payload["repository"]
        owner = repo_info["owner"]["login"]
        repo_name = repo_info["name"]
        pr_number = pr["number"]

        # 异步处理 PR
        from threading import Thread
        Thread(target=handle_pull_request, args=(owner, repo_name, pr_number)).start()

    return "", 204
