import requests
import json
import hmac
import hashlib
import logging
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import threading
import time

class GitHubWebhookHandler:
    """
    GitHub Webhook 处理器，用于接收和处理 GitHub PR 事件
    """
    
    def __init__(self, repo_url, github_token, webhook_secret):
        """
        初始化 GitHub Webhook 处理器
        
        Args:
            repo_url (str): GitHub 仓库地址
            github_token (str): GitHub Token
            webhook_secret (str): GitHub Webhook Secret
        """
        self.repo_url = repo_url
        self.github_token = github_token
        self.webhook_secret = webhook_secret
        self.app = Flask(__name__)
        self.server_thread = None
        self.is_running = False
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 设置 Flask 路由
        self._setup_routes()
    
    def _setup_routes(self):
        """设置 Flask 路由"""
        
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            """
            处理 GitHub Webhook 请求
            
            Returns:
                json: 响应结果
            """
            try:
                # 验证 webhook 签名
                if not self._verify_signature(request):
                    self.logger.error("Webhook 签名验证失败")
                    return jsonify({"error": "签名验证失败"}), 401
                
                # 解析事件类型
                event_type = request.headers.get('X-GitHub-Event')
                payload = request.json
                
                self.logger.info(f"收到 GitHub 事件: {event_type}")
                
                # 处理 PR 事件
                if event_type == 'pull_request':
                    return self._handle_pull_request(payload)
                else:
                    self.logger.info(f"忽略事件类型: {event_type}")
                    return jsonify({"message": "事件已接收"}), 200
                    
            except Exception as e:
                self.logger.error(f"处理 webhook 时发生错误: {str(e)}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/health', methods=['GET'])
        def health():
            """健康检查端点"""
            return jsonify({"status": "healthy", "service": "github_webhook_handler"}), 200
    
    def _verify_signature(self, request):
        """
        验证 GitHub Webhook 签名
        
        Args:
            request: Flask 请求对象
            
        Returns:
            bool: 验证是否成功
        """
        if not self.webhook_secret:
            return True  # 如果没有设置 secret，跳过验证
        
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            return False
        
        # 计算预期签名
        expected_signature = 'sha256=' + hmac.new(
            self.webhook_secret.encode('utf-8'),
            request.data,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _handle_pull_request(self, payload):
        """
        处理 Pull Request 事件
        
        Args:
            payload (dict): GitHub 事件负载
            
        Returns:
            json: 响应结果
        """
        try:
            action = payload.get('action')
            pr_data = payload.get('pull_request', {})
            
            self.logger.info(f"处理 PR 事件: {action}")
            
            # 只处理 opened 和 synchronize 事件
            if action not in ['opened', 'synchronize']:
                return jsonify({"message": f"忽略 PR 事件: {action}"}), 200
            
            # 提取 PR 信息
            pr_info = self._extract_pr_info(pr_data)
            
            # 觸發回調函數
            if hasattr(self, 'on_pr_event'):
                self.on_pr_event(pr_info)
            
            return jsonify({"message": "PR 事件处理成功"}), 200
            
        except Exception as e:
            self.logger.error(f"处理 PR 事件时发生错误: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def _extract_pr_info(self, pr_data):
        """
        从 PR 数据中提取信息
        
        Args:
            pr_data (dict): PR 数据
            
        Returns:
            dict: 提取的 PR 信息
        """
        return {
            'title': pr_data.get('title', ''),
            'description': pr_data.get('body', ''),
            'author': pr_data.get('user', {}).get('login', ''),
            'author_name': pr_data.get('user', {}).get('name', ''),
            'number': pr_data.get('number', 0),
            'url': pr_data.get('html_url', ''),
            'state': pr_data.get('state', ''),
            'created_at': pr_data.get('created_at', ''),
            'updated_at': pr_data.get('updated_at', ''),
            'base_branch': pr_data.get('base', {}).get('ref', ''),
            'head_branch': pr_data.get('head', {}).get('ref', ''),
            'additions': pr_data.get('additions', 0),
            'deletions': pr_data.get('deletions', 0),
            'changed_files': pr_data.get('changed_files', 0)
        }
    
    def _get_pr_files(self, pr_number):
        """
        获取 PR 修改的文件列表
        
        Args:
            pr_number (int): PR 编号
            
        Returns:
            list: 修改的文件列表
        """
        try:
            # 解析仓库信息
            repo_path = urlparse(self.repo_url).path.strip('/')
            
            # 构建 API URL
            api_url = f"https://api.github.com/repos/{repo_path}/pulls/{pr_number}/files"
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            files = response.json()
            return [file['filename'] for file in files]
            
        except Exception as e:
            self.logger.error(f"获取 PR 文件列表失败: {str(e)}")
            return []
    
    def start_webhook_server(self, feishu_handler=None, ai_summarizer=None):
        """
        启动 Webhook 服务器
        
        Args:
            feishu_handler: 飞书处理器实例
            ai_summarizer: AI 总结器实例
        """
        if self.is_running:
            self.logger.warning("Webhook 服务器已在运行中")
            return
        
        # 设置回调函数
        def on_pr_event(pr_info):
            """PR 事件回调函数"""
            try:
                self.logger.info(f"处理 PR #{pr_info['number']}: {pr_info['title']}")
                
                # 获取修改的文件
                changed_files = self._get_pr_files(pr_info['number'])
                pr_info['changed_files_list'] = changed_files
                
                # 使用 AI 总结 PR 内容
                if ai_summarizer:
                    summary = ai_summarizer.summarize_pr(pr_info)
                    self.logger.info(f"AI 总结完成: {summary[:100]}...")
                    
                    # 发送到飞书
                    if feishu_handler:
                        feishu_handler.send_summary(summary, pr_info)
                        self.logger.info("总结已发送到飞书")
                    else:
                        self.logger.warning("飞书处理器未配置")
                else:
                    self.logger.warning("AI 总结器未配置")
                    
            except Exception as e:
                self.logger.error(f"处理 PR 事件时发生错误: {str(e)}")
        
        self.on_pr_event = on_pr_event
        self.is_running = True
        
        # 启动 Flask 服务器
        self.logger.info("启动 Webhook 服务器...")
        self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
    def stop_webhook_server(self):
        """停止 Webhook 服务器"""
        if not self.is_running:
            self.logger.warning("Webhook 服务器未在运行")
            return
        
        self.is_running = False
        self.logger.info("Webhook 服务器已停止")
    
    def get_webhook_url(self):
        """
        获取 Webhook URL
        
        Returns:
            str: Webhook URL
        """
        return "http://your-domain.com/webhook"  # 需要替换为实际的域名 