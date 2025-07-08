# �������ļ������� Flask + Gradio

import gradio as gr
import openai
from flask import Flask, request, abort
from threading import Thread
import hmac, hashlib, json
from github import Github

# ====== ���ò��� ======
WEBHOOK_SECRET = b"���WebhookSecret"  # GitHub Webhook �����е� Secret
GITHUB_TOKEN = "���GitHub��������"
openai.api_key = "���OpenAI API Key"
# ======================

# ��ʼ�� Flask �� GitHub �ͻ���
app = Flask(__name__)
g = Github(GITHUB_TOKEN)

# === OpenAI �ܽắ�� ===
def summarize_code(diff: str):
    """������ diff ת��Ϊ��Ȼ����ժҪ"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "developer", "content": "�뽫���´������ܽ�Ϊ��Ҫ˵��:"},
            {"role": "user", "content": diff}
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content

# === Gradio MCP �ӿ� ===
gradio_interface = gr.Interface(
    fn=summarize_code,
    inputs=gr.Textbox(lines=10, placeholder="������ diff"),
    outputs="text",
    title="������ժҪ",
    description="���� GitHub PR �Ĵ����� diff�������Ȼ����ժҪ"
)

# === ���� PR �������� ===
def handle_pull_request(owner, repo_name, pr_number):
    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)
    files = pr.get_files()
    
    diff_text = ""
    for f in files:
        diff_text += f"File: {f.filename}\n{f.patch}\n\n"

    summary = summarize_code(diff_text)
    print(f"? PR #{pr_number} Summary:\n{summary}\n")
    # TODO: ��д����־����Ϊ����д�� PR

# === Webhook ����·�� ===
@app.route("/webhook", methods=["POST"])
def github_webhook():
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = request.data

    mac = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256)
    expected_signature = "sha256=" + mac.hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        abort(400, "Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")
    payload = json.loads(body)
    action = payload.get("action", "")

    if event == "pull_request" and action in ("opened", "synchronize", "ready_for_review"):
        pr = payload["pull_request"]
        owner = payload["repository"]["owner"]["login"]
        repo = payload["repository"]["name"]
        pr_number = pr["number"]

        # �첽���� PR����������
        Thread(target=handle_pull_request, args=(owner, repo, pr_number)).start()

    return "", 204

# === �������� ===
def run_all():
    # ���� Flask
    def run_flask():
        app.run(host="0.0.0.0", port=7861)
    
    # ���� Gradio MCP Server
    def run_gradio():
        gradio_interface.launch(server_name="0.0.0.0", server_port=7860, mcp_server=True)
    
    # ������������
    Thread(target=run_flask).start()
    run_gradio()

# === ��ڵ� ===
if __name__ == "__main__":
    run_all()
