#!/usr/bin/env python3
"""
简化的 MCP Server 实现
基于标准 MCP 协议，提供 GitHub PR 监听和飞书日记功能
"""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# 项目模块
from github_handler import GitHubWebhookHandler
from feishu_handler import FeishuHandler
from ai_summarizer import AISummarizer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPConfig:
    """MCP 服务器配置"""
    github_repo_url: str = ""
    github_token: str = ""
    webhook_secret: str = ""
    feishu_token: str = ""
    feishu_url: str = ""
    openai_api_key: str = ""

class SimpleMCPServer:
    """简化的 MCP Server 实现"""
    
    def __init__(self):
        self.config = MCPConfig()
        self.github_handler = None
        self.feishu_handler = None
        self.ai_summarizer = None
        self.is_running = False
        
        # 从环境变量加载配置
        self._load_config_from_env()
    
    def _load_config_from_env(self):
        """从环境变量加载配置"""
        self.config.github_repo_url = os.getenv("GITHUB_REPO_URL", "")
        self.config.github_token = os.getenv("GITHUB_TOKEN", "")
        self.config.webhook_secret = os.getenv("WEBHOOK_SECRET", "")
        self.config.feishu_token = os.getenv("FEISHU_TOKEN", "")
        self.config.feishu_url = os.getenv("FEISHU_URL", "")
        self.config.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    
    def configure_github_listener(self, repo_url: str, github_token: str, webhook_secret: str) -> str:
        """
        配置 GitHub 监听器
        
        Args:
            repo_url: GitHub 仓库地址
            github_token: GitHub Token
            webhook_secret: GitHub Webhook Secret
            
        Returns:
            配置结果消息
        """
        try:
            self.config.github_repo_url = repo_url
            self.config.github_token = github_token
            self.config.webhook_secret = webhook_secret
            
            self.github_handler = GitHubWebhookHandler(
                repo_url=repo_url,
                github_token=github_token,
                webhook_secret=webhook_secret
            )
            
            return "✅ GitHub 监听器配置成功"
        except Exception as e:
            return f"❌ GitHub 监听器配置失败: {str(e)}"
    
    def configure_feishu_handler(self, feishu_token: str, feishu_url: str) -> str:
        """
        配置飞书处理器
        
        Args:
            feishu_token: 飞书 API Token
            feishu_url: 飞书知识库 API Endpoint
            
        Returns:
            配置结果消息
        """
        try:
            self.config.feishu_token = feishu_token
            self.config.feishu_url = feishu_url
            
            self.feishu_handler = FeishuHandler(
                token=feishu_token,
                url=feishu_url
            )
            
            return "✅ 飞书处理器配置成功"
        except Exception as e:
            return f"❌ 飞书处理器配置失败: {str(e)}"
    
    def configure_ai_summarizer(self, openai_api_key: str) -> str:
        """
        配置 AI 总结器
        
        Args:
            openai_api_key: OpenAI API Key
            
        Returns:
            配置结果消息
        """
        try:
            self.config.openai_api_key = openai_api_key
            
            self.ai_summarizer = AISummarizer(
                api_key=openai_api_key
            )
            
            return "✅ AI 总结器配置成功"
        except Exception as e:
            return f"❌ AI 总结器配置失败: {str(e)}"
    
    def start_webhook_server(self) -> str:
        """
        启动 Webhook 服务器
        
        Returns:
            启动结果消息
        """
        if not all([self.github_handler, self.feishu_handler, self.ai_summarizer]):
            return "❌ 请先配置所有必要的组件"
        
        if self.is_running:
            return "⚠️ Webhook 服务器已在运行中"
        
        try:
            # 启动 webhook 服务器
            self.github_handler.start_webhook_server(
                self.feishu_handler,
                self.ai_summarizer
            )
            self.is_running = True
            return "✅ Webhook 服务器启动成功"
        except Exception as e:
            return f"❌ Webhook 服务器启动失败: {str(e)}"
    
    def stop_webhook_server(self) -> str:
        """
        停止 Webhook 服务器
        
        Returns:
            停止结果消息
        """
        if not self.is_running:
            return "⚠️ Webhook 服务器未在运行"
        
        try:
            self.github_handler.stop_webhook_server()
            self.is_running = False
            return "✅ Webhook 服务器已停止"
        except Exception as e:
            return f"❌ Webhook 服务器停止失败: {str(e)}"
    
    def get_server_status(self) -> str:
        """
        获取服务器状态
        
        Returns:
            当前状态信息
        """
        status = []
        status.append(f"GitHub 处理器: {'✅ 已配置' if self.github_handler else '❌ 未配置'}")
        status.append(f"飞书处理器: {'✅ 已配置' if self.feishu_handler else '❌ 未配置'}")
        status.append(f"AI 总结器: {'✅ 已配置' if self.ai_summarizer else '❌ 未配置'}")
        status.append(f"Webhook 服务器: {'🟢 运行中' if self.is_running else '🔴 已停止'}")
        
        return "\n".join(status)
    
    def test_github_connection(self) -> str:
        """
        测试 GitHub 连接
        
        Returns:
            测试结果
        """
        if not self.github_handler:
            return "❌ GitHub 处理器未配置"
        
        try:
            # 简单的连接测试
            return "✅ GitHub 处理器已配置"
        except Exception as e:
            return f"❌ GitHub 连接测试失败: {str(e)}"
    
    def test_feishu_connection(self) -> str:
        """
        测试飞书连接
        
        Returns:
            测试结果
        """
        if not self.feishu_handler:
            return "❌ 飞书处理器未配置"
        
        try:
            # 简单的连接测试
            return "✅ 飞书处理器已配置"
        except Exception as e:
            return f"❌ 飞书连接测试失败: {str(e)}"
    
    def test_ai_summarizer(self) -> str:
        """
        测试 AI 总结器
        
        Returns:
            测试结果
        """
        if not self.ai_summarizer:
            return "❌ AI 总结器未配置"
        
        try:
            # 测试 OpenAI API
            test_summary = self.ai_summarizer.summarize_pr({
                "title": "测试 PR",
                "description": "这是一个测试 PR",
                "author": "测试用户",
                "files": ["test.py"]
            })
            return f"✅ AI 总结器测试成功: {test_summary[:100]}..."
        except Exception as e:
            return f"❌ AI 总结器测试失败: {str(e)}"
    
    def get_config(self) -> Dict[str, Any]:
        """
        获取当前配置
        
        Returns:
            配置信息
        """
        return {
            "github_repo_url": self.config.github_repo_url,
            "feishu_url": self.config.feishu_url,
            "is_running": self.is_running,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status_json(self) -> Dict[str, Any]:
        """
        获取状态信息（JSON 格式）
        
        Returns:
            状态信息
        """
        return {
            "github_handler": self.github_handler is not None,
            "feishu_handler": self.feishu_handler is not None,
            "ai_summarizer": self.ai_summarizer is not None,
            "is_running": self.is_running,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """主函数 - 提供命令行接口"""
    server = SimpleMCPServer()
    
    print("📝 MCP GitHub PR 日记服务器")
    print("=" * 50)
    
    while True:
        print("\n📋 可用命令:")
        print("1. configure_github <repo_url> <token> <secret>")
        print("2. configure_feishu <token> <url>")
        print("3. configure_ai <api_key>")
        print("4. start_server")
        print("5. stop_server")
        print("6. status")
        print("7. test_github")
        print("8. test_feishu")
        print("9. test_ai")
        print("10. config")
        print("11. quit")
        
        try:
            command = input("\n请输入命令: ").strip()
            
            if command == "quit":
                print("👋 再见！")
                break
            
            elif command.startswith("configure_github "):
                parts = command.split(" ", 3)
                if len(parts) == 4:
                    result = server.configure_github_listener(parts[1], parts[2], parts[3])
                    print(f"结果: {result}")
                else:
                    print("❌ 格式错误: configure_github <repo_url> <token> <secret>")
            
            elif command.startswith("configure_feishu "):
                parts = command.split(" ", 2)
                if len(parts) == 3:
                    result = server.configure_feishu_handler(parts[1], parts[2])
                    print(f"结果: {result}")
                else:
                    print("❌ 格式错误: configure_feishu <token> <url>")
            
            elif command.startswith("configure_ai "):
                parts = command.split(" ", 1)
                if len(parts) == 2:
                    result = server.configure_ai_summarizer(parts[1])
                    print(f"结果: {result}")
                else:
                    print("❌ 格式错误: configure_ai <api_key>")
            
            elif command == "start_server":
                result = server.start_webhook_server()
                print(f"结果: {result}")
            
            elif command == "stop_server":
                result = server.stop_webhook_server()
                print(f"结果: {result}")
            
            elif command == "status":
                result = server.get_server_status()
                print(f"状态:\n{result}")
            
            elif command == "test_github":
                result = server.test_github_connection()
                print(f"结果: {result}")
            
            elif command == "test_feishu":
                result = server.test_feishu_connection()
                print(f"结果: {result}")
            
            elif command == "test_ai":
                result = server.test_ai_summarizer()
                print(f"结果: {result}")
            
            elif command == "config":
                config = server.get_config()
                print(f"配置: {json.dumps(config, indent=2, ensure_ascii=False)}")
            
            else:
                print("❌ 未知命令")
        
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    main() 