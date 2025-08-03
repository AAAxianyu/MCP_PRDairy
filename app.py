import gradio as gr
import os
import json
import threading
from dotenv import load_dotenv
from github_handler import GitHubWebhookHandler
from feishu_handler import FeishuHandler
from ai_summarizer import AISummarizer

# 载入环境变量
load_dotenv()

class MCPPRDairyServer:
    """
    MCP Server 用于监听 GitHub PR 事件并将总结发送到飞书知识库
    """
    
    def __init__(self):
        self.github_handler = None
        self.feishu_handler = None
        self.ai_summarizer = None
        self.webhook_thread = None
        self.is_running = False
        
    def configure_github_listener(self, repo_url, github_token, webhook_secret):
        """
        配置 GitHub 监听器
        
        Args:
            repo_url (str): GitHub 仓库地址
            github_token (str): GitHub Token
            webhook_secret (str): GitHub Webhook Secret
            
        Returns:
            str: 配置结果消息
        """
        try:
            self.github_handler = GitHubWebhookHandler(
                repo_url=repo_url,
                github_token=github_token,
                webhook_secret=webhook_secret
            )
            return "✅ GitHub 监听器配置成功"
        except Exception as e:
            return f"❌ GitHub 监听器配置失败: {str(e)}"
    
    def configure_feishu_handler(self, feishu_token, feishu_url):
        """
        配置飞书处理器
        
        Args:
            feishu_token (str): 飞书 API Token
            feishu_url (str): 飞书知识库 API Endpoint
            
        Returns:
            str: 配置结果消息
        """
        try:
            self.feishu_handler = FeishuHandler(
                token=feishu_token,
                url=feishu_url
            )
            return "✅ 飞书处理器配置成功"
        except Exception as e:
            return f"❌ 飞书处理器配置失败: {str(e)}"
    
    def configure_ai_summarizer(self, openai_api_key):
        """
        配置 AI 总结器
        
        Args:
            openai_api_key (str): OpenAI API Key
            
        Returns:
            str: 配置结果消息
        """
        try:
            self.ai_summarizer = AISummarizer(api_key=openai_api_key)
            return "✅ AI 总结器配置成功"
        except Exception as e:
            return f"❌ AI 总结器配置失败: {str(e)}"
    
    def start_webhook_server(self):
        """
        启动 Webhook 服务器
        
        Returns:
            str: 启动结果消息
        """
        if not all([self.github_handler, self.feishu_handler, self.ai_summarizer]):
            return "❌ 请先配置所有必要的组件"
        
        if self.is_running:
            return "⚠️ Webhook 服务器已在运行中"
        
        try:
            self.webhook_thread = threading.Thread(
                target=self.github_handler.start_webhook_server,
                args=(self.feishu_handler, self.ai_summarizer)
            )
            self.webhook_thread.daemon = True
            self.webhook_thread.start()
            self.is_running = True
            return "✅ Webhook 服务器启动成功"
        except Exception as e:
            return f"❌ Webhook 服务器启动失败: {str(e)}"
    
    def stop_webhook_server(self):
        """
        停止 Webhook 服务器
        
        Returns:
            str: 停止结果消息
        """
        if not self.is_running:
            return "⚠️ Webhook 服务器未在运行"
        
        try:
            self.github_handler.stop_webhook_server()
            self.is_running = False
            return "✅ Webhook 服务器已停止"
        except Exception as e:
            return f"❌ Webhook 服务器停止失败: {str(e)}"
    
    def get_status(self):
        """
        获取服务器状态
        
        Returns:
            str: 当前状态信息
        """
        status = []
        status.append(f"GitHub 处理器: {'✅ 已配置' if self.github_handler else '❌ 未配置'}")
        status.append(f"飞书处理器: {'✅ 已配置' if self.feishu_handler else '❌ 未配置'}")
        status.append(f"AI 总结器: {'✅ 已配置' if self.ai_summarizer else '❌ 未配置'}")
        status.append(f"Webhook 服务器: {'🟢 运行中' if self.is_running else '🔴 已停止'}")
        
        return "\n".join(status)

def create_interface():
    """
    创建 Gradio 界面
    
    Returns:
        gr.Interface: Gradio 界面对象
    """
    server = MCPPRDairyServer()
    
    with gr.Blocks(title="MCP GitHub PR 日记服务器", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 📝 MCP GitHub PR 日记服务器")
        gr.Markdown("### MCP&Agent挑战赛 - MCP_Agent_Challenge")
        gr.Markdown("监听 GitHub PR 事件并将 AI 总结发送到飞书知识库")
        
        with gr.Tab("配置"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### GitHub 配置")
                    repo_url = gr.Textbox(
                        label="GitHub 仓库地址",
                        placeholder="https://github.com/username/repo",
                        value=os.getenv("GITHUB_REPO_URL", "")
                    )
                    github_token = gr.Textbox(
                        label="GitHub Token",
                        type="password",
                        value=os.getenv("GITHUB_TOKEN", "")
                    )
                    webhook_secret = gr.Textbox(
                        label="GitHub Webhook Secret",
                        type="password",
                        value=os.getenv("WEBHOOK_SECRET", "")
                    )
                    github_config_btn = gr.Button("配置 GitHub 监听器", variant="primary")
                    github_status = gr.Textbox(label="GitHub 配置状态", interactive=False)
                
                with gr.Column():
                    gr.Markdown("### 飞书配置")
                    feishu_token = gr.Textbox(
                        label="飞书 API Token",
                        type="password",
                        value=os.getenv("FEISHU_TOKEN", "")
                    )
                    feishu_url = gr.Textbox(
                        label="飞书知识库 API Endpoint",
                        placeholder="https://open.feishu.cn/open-apis/docx/v1/spaces/xxx",
                        value=os.getenv("FEISHU_URL", "")
                    )
                    feishu_config_btn = gr.Button("配置飞书处理器", variant="primary")
                    feishu_status = gr.Textbox(label="飞书配置状态", interactive=False)
                
                with gr.Column():
                    gr.Markdown("### AI 配置")
                    openai_api_key = gr.Textbox(
                        label="OpenAI API Key",
                        type="password",
                        value=os.getenv("OPENAI_API_KEY", "")
                    )
                    ai_config_btn = gr.Button("配置 AI 总结器", variant="primary")
                    ai_status = gr.Textbox(label="AI 配置状态", interactive=False)
        
        with gr.Tab("控制"):
            with gr.Row():
                start_btn = gr.Button("🚀 启动 Webhook 服务器", variant="primary", size="lg")
                stop_btn = gr.Button("🛑 停止 Webhook 服务器", variant="stop", size="lg")
                status_btn = gr.Button("📊 查看状态", size="lg")
            
            status_output = gr.Textbox(label="服务器状态", interactive=False, lines=5)
        
        with gr.Tab("日志"):
            log_output = gr.Textbox(label="运行日志", interactive=False, lines=20)
        
        # 事件处理
        github_config_btn.click(
            server.configure_github_listener,
            inputs=[repo_url, github_token, webhook_secret],
            outputs=github_status
        )
        
        feishu_config_btn.click(
            server.configure_feishu_handler,
            inputs=[feishu_token, feishu_url],
            outputs=feishu_status
        )
        
        ai_config_btn.click(
            server.configure_ai_summarizer,
            inputs=[openai_api_key],
            outputs=ai_status
        )
        
        start_btn.click(
            server.start_webhook_server,
            outputs=status_output
        )
        
        stop_btn.click(
            server.stop_webhook_server,
            outputs=status_output
        )
        
        status_btn.click(
            server.get_status,
            outputs=status_output
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        mcp_server=True,
    ) 