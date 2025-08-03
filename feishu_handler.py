import requests
import json
import logging
from datetime import datetime

class FeishuHandler:
    """
    飞书处理器，用于将 PR 总结发送到飞书知识库
    """
    
    def __init__(self, token, url):
        """
        初始化飞书处理器
        
        Args:
            token (str): 飞书 API Token
            url (str): 飞书知识库 API Endpoint
        """
        self.token = token
        self.url = url
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def send_summary(self, summary, pr_info):
        """
        发送总结到飞书知识库
        
        Args:
            summary (str): AI 生成的总结
            pr_info (dict): PR 信息
            
        Returns:
            bool: 发送是否成功
        """
        try:
            # 构建文档内容
            document_content = self._build_document_content(summary, pr_info)
            
            # 发送到飞书
            success = self._send_to_feishu(document_content)
            
            if success:
                self.logger.info(f"总结已成功发送到飞书知识库")
            else:
                self.logger.error("发送到飞书失败")
            
            return success
            
        except Exception as e:
            self.logger.error(f"发送总结到飞书时发生错误: {str(e)}")
            return False
    
    def _build_document_content(self, summary, pr_info):
        """
        构建飞书文档内容
        
        Args:
            summary (str): AI 生成的总结
            pr_info (dict): PR 信息
            
        Returns:
            dict: 文档内容结构
        """
        # 格式化时间
        created_time = datetime.fromisoformat(pr_info['created_at'].replace('Z', '+00:00'))
        formatted_time = created_time.strftime('%Y年%m月%d日 %H:%M')
        
        # 构建文件列表
        files_text = ""
        if pr_info.get('changed_files_list'):
            files_text = "\n".join([f"• {file}" for file in pr_info['changed_files_list'][:10]])
            if len(pr_info['changed_files_list']) > 10:
                files_text += f"\n... 还有 {len(pr_info['changed_files_list']) - 10} 个文件"
        
        # 构建文档内容
        content = {
            "blocks": [
                {
                    "type": "heading1",
                    "heading1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"📝 开发日记 - PR #{pr_info['number']}"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": summary
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "divider",
                    "divider": {}
                },
                {
                    "type": "heading2",
                    "heading2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "📋 PR 详细信息"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "table",
                    "table": {
                        "table_width": 2,
                        "rows": [
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "标题"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": pr_info['title']}}]}
                                ]
                            },
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "作者"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": f"{pr_info['author']} ({pr_info.get('author_name', '')})"}}]}
                                ]
                            },
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "创建时间"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": formatted_time}}]}
                                ]
                            },
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "分支"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": f"{pr_info['head_branch']} → {pr_info['base_branch']}"}}]}
                                ]
                            },
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "统计"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": f"+{pr_info['additions']} -{pr_info['deletions']} ({pr_info['changed_files']} 个文件)"}}]}
                                ]
                            },
                            {
                                "cells": [
                                    {"rich_text": [{"type": "text", "text": {"content": "链接"}}]},
                                    {"rich_text": [{"type": "text", "text": {"content": pr_info['url']}}]}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
        
        # 如果有修改的文件，添加文件列表
        if files_text:
            content["blocks"].extend([
                {
                    "type": "heading2",
                    "heading2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "📁 修改的文件"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": files_text
                                }
                            }
                        ]
                    }
                }
            ])
        
        return content
    
    def _send_to_feishu(self, content):
        """
        发送到飞书知识库
        
        Args:
            content (dict): 文档内容
            
        Returns:
            bool: 发送是否成功
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # 构建请求数据
            data = {
                "document": {
                                         "document_id": "auto",  # 自动生成文档 ID
                                         "title": f"开发日记 - {datetime.now().strftime('%Y年%m月%d日')}",
                    "content": content
                }
            }
            
            # 发送请求
            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"飞书文档创建成功: {result.get('data', {}).get('document_id', 'unknown')}")
                return True
            else:
                self.logger.error(f"飞书 API 请求失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"发送到飞书时发生错误: {str(e)}")
            return False
    
    def test_connection(self):
        """
        测试飞书 API 连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            # 测试请求
            response = requests.get(
                self.url.replace('/documents', '/spaces'),
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"飞书 API 连接测试失败: {str(e)}")
            return False
    
    def create_test_document(self):
        """
        创建测试文档
        
        Returns:
            bool: 创建是否成功
        """
        test_content = {
            "blocks": [
                {
                    "type": "heading1",
                    "heading1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "🧪 测试文档"
                                }
                            }
                        ]
                    }
                },
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "这是一个测试文档，用于验证飞书 API 连接是否正常。"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        return self._send_to_feishu(test_content) 