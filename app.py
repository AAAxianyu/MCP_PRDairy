from flask import Flask
from threading import Thread
from webhook_handler import github_webhook
import gradio as gr
from summarizer import summarize_code  # 现在这个函数已经集成了飞书发送功能

app = Flask(__name__)
app.add_url_rule("/webhook", view_func=github_webhook, methods=["POST"])

# Gradio MCP Server
demo = gr.Interface(
    fn=summarize_code,
    inputs=gr.Textbox(lines=10, placeholder="输入 GitHub PR 的 diff 内容"),
    outputs="text",
    title="GitHub PR 摘要生成",
    description="输入 GitHub diff，输出自然语言总结"
)

def run_flask():
    app.run(host="0.0.0.0", port=7861)

def run_gradio():
    demo.launch(server_name="0.0.0.0", server_port=7860, mcp_server=True)

def run_all():
    Thread(target=run_flask).start()
    run_gradio()

if __name__ == "__main__":
    run_all()
