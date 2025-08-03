#!/usr/bin/env python3
"""
测试服务器 - 用于测试 MCP GitHub PR 日记服务器的各个组件
"""

import json
import requests
from datetime import datetime
from ai_summarizer import AISummarizer
from feishu_handler import FeishuHandler

def test_ai_summarizer():
    """测试 AI 总结器"""
    print("🧪 测试 AI 总结器...")
    
    # 模拟 PR 信息
    test_pr_info = {
        'title': '优化用户登录功能',
        'description': '新增双因子认证支持，改进密码验证逻辑，修复登录页面响应式布局问题',
        'author': 'zhangsan',
        'author_name': '张三',
        'number': 123,
        'url': 'https://github.com/test/repo/pull/123',
        'state': 'open',
        'created_at': '2024-01-15T10:30:00Z',
        'updated_at': '2024-01-15T10:30:00Z',
        'base_branch': 'main',
        'head_branch': 'feature/login-optimization',
        'additions': 120,
        'deletions': 45,
        'changed_files': 5,
        'changed_files_list': [
            'src/auth/login.js',
            'src/auth/validation.js',
            'src/components/LoginForm.jsx',
            'tests/auth.test.js',
            'docs/login-api.md'
        ]
    }
    
    try:
        # 注意：这里需要有效的 OpenAI API Key
        # summarizer = AISummarizer(api_key="your_openai_api_key")
        # summary = summarizer.summarize_pr(test_pr_info)
        
        # 使用备用总结方法进行测试
        summarizer = AISummarizer(api_key="test_key")
        summary = summarizer._fallback_summary(test_pr_info)
        
        print(f"✅ AI 总结测试成功")
        print(f"📝 总结内容: {summary}")
        return True
        
    except Exception as e:
        print(f"❌ AI 总结测试失败: {str(e)}")
        return False

def test_feishu_handler():
    """测试飞书处理器"""
    print("\n🧪 测试飞书处理器...")
    
    # 模拟数据
    test_summary = "今天 张三 提交了一个 PR (#123)，主要完成了用户登录功能的优化。新增了双因子认证支持，改进了密码验证逻辑，并修复了登录页面的响应式布局问题。共修改了 5 个文件，新增 120 行，删除 45 行。"
    
    test_pr_info = {
        'title': '优化用户登录功能',
        'author': 'zhangsan',
        'author_name': '张三',
        'number': 123,
        'url': 'https://github.com/test/repo/pull/123',
        'created_at': '2024-01-15T10:30:00Z',
        'base_branch': 'main',
        'head_branch': 'feature/login-optimization',
        'additions': 120,
        'deletions': 45,
        'changed_files': 5,
        'changed_files_list': [
            'src/auth/login.js',
            'src/auth/validation.js',
            'src/components/LoginForm.jsx'
        ]
    }
    
    try:
        # 注意：这里需要有效的飞书 Token 和 URL
        # handler = FeishuHandler(token="your_feishu_token", url="your_feishu_url")
        # success = handler.send_summary(test_summary, test_pr_info)
        
        # 测试文档内容构建
        handler = FeishuHandler(token="test_token", url="test_url")
        content = handler._build_document_content(test_summary, test_pr_info)
        
        print(f"✅ 飞书处理器测试成功")
        print(f"📄 文档内容结构: {len(content['blocks'])} 个区块")
        return True
        
    except Exception as e:
        print(f"❌ 飞书处理器测试失败: {str(e)}")
        return False

def test_github_webhook():
    """测试 GitHub Webhook 处理"""
    print("\n🧪 测试 GitHub Webhook 处理...")
    
    # 模拟 GitHub Webhook 请求
    test_payload = {
        "action": "opened",
        "pull_request": {
            "title": "测试 PR",
            "body": "这是一个测试 PR",
            "user": {
                "login": "testuser",
                "name": "测试用户"
            },
            "number": 999,
            "html_url": "https://github.com/test/repo/pull/999",
            "state": "open",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "base": {"ref": "main"},
            "head": {"ref": "test-branch"},
            "additions": 50,
            "deletions": 10,
            "changed_files": 3
        }
    }
    
    try:
        # 测试 PR 信息提取
        from github_handler import GitHubWebhookHandler
        
        handler = GitHubWebhookHandler(
            repo_url="https://github.com/test/repo",
            github_token="test_token",
            webhook_secret="test_secret"
        )
        
        pr_info = handler._extract_pr_info(test_payload['pull_request'])
        
        print(f"✅ GitHub Webhook 处理测试成功")
        print(f"📋 提取的 PR 信息: {pr_info['title']} by {pr_info['author']}")
        return True
        
    except Exception as e:
        print(f"❌ GitHub Webhook 处理测试失败: {str(e)}")
        return False

def test_mcp_server():
    """测试 MCP 服务器功能"""
    print("\n🧪 测试 MCP 服务器功能...")
    
    try:
        from main import MCPPRDairyServer
        
        server = MCPPRDairyServer()
        
        # 测试配置方法
        github_result = server.configure_github_listener(
            "https://github.com/test/repo",
            "test_token",
            "test_secret"
        )
        
        feishu_result = server.configure_feishu_handler(
            "test_token",
            "https://test.feishu.cn/api"
        )
        
        ai_result = server.configure_ai_summarizer("test_api_key")
        
        status = server.get_status()
        
        print(f"✅ MCP 服务器功能测试成功")
        print(f"📊 服务器状态:\n{status}")
        return True
        
    except Exception as e:
        print(f"❌ MCP 服务器功能测试失败: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行 MCP GitHub PR 日记服务器测试套件")
    print("=" * 60)
    
    tests = [
        ("AI 总结器", test_ai_summarizer),
        ("飞书处理器", test_feishu_handler),
        ("GitHub Webhook 处理", test_github_webhook),
        ("MCP 服务器功能", test_mcp_server)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！服务器准备就绪。")
    else:
        print("⚠️ 部分测试失败，请检查配置和依赖。")

if __name__ == "__main__":
    run_all_tests() 