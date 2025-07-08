# 主启动文件，整合 Flask + Gradio
import gradio as gr
import openai
from flask import Flask, request, abort
from threading import Thread
import hmac, hashlib, json
from github import Github

# ====== 配置部分 ======
WEBHOOK_SECRET = b"你的WebhookSecret"  # GitHub Webhook 设置中的 Secret
GITHUB_TOKEN = "你的GitHub访问令牌"
openai.api_key = "你的OpenAI API Key"
# ======================

# 初始化 Flask 和 GitHub 客户端
app = Flask(__name__)
g = Github(GITHUB_TOKEN)

# === OpenAI 总结函数 ===
def summarize_code(diff: str):
    """将代码 diff 转化为自然语言摘要"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "developer", "content": "请将以下代码变更总结为简要说明:"},
            {"role": "user", "content": diff}
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content

# === Gradio MCP 接口 ===
gradio_interface = gr.Interface(
    fn=summarize_code,
    inputs=gr.Textbox(lines=10, placeholder="代码变更 diff"),
    outputs="text",
    title="代码变更摘要",
    description="输入 GitHub PR 的代码变更 diff，输出自然语言摘要"
)

# === 处理 PR 的主函数 ===
def handle_pull_request(owner, repo_name, pr_number):
    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)
    files = pr.get_files()
    
    diff_text = ""
    for f in files:
        diff_text += f"File: {f.filename}\n{f.patch}\n\n"

    summary = summarize_code(diff_text)
    print(f"✅ PR #{pr_number} Summary:\n{summary}\n")
    # TODO: 可写入日志或作为评论写回 PR

# === Webhook 接收路由 ===
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

        # 异步处理 PR，避免阻塞
        Thread(target=handle_pull_request, args=(owner, repo, pr_number)).start()

    return "", 204

# === 启动函数 ===
def run_all():
    # 启动 Flask
    def run_flask():
        app.run(host="0.0.0.0", port=7861)
    
    # 启动 Gradio MCP Server
    def run_gradio():
        gradio_interface.launch(server_name="0.0.0.0", server_port=7860, mcp_server=True)
    
    # 启动两个服务
    Thread(target=run_flask).start()
    run_gradio()

# === 入口点 ===
if __name__ == "__main__":
    run_all()
