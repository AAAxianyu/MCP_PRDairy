#!/usr/bin/env python3
"""
GitHub PR MCP Server 构建和发布脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """运行命令并处理错误"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    # 删除构建目录
    build_dirs = ['build', 'dist', 'src/github_pr_mcp_server.egg-info']
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 删除 {dir_name}")
    
    # 删除 Python 缓存
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_dir = os.path.join(root, dir_name)
                shutil.rmtree(cache_dir)
                print(f"✅ 删除缓存: {cache_dir}")


def build_package():
    """构建包"""
    print("📦 构建包...")
    
    # 检查必要文件
    required_files = [
        'pyproject.toml',
        'README.md',
        'src/github_pr_mcp_server/__init__.py',
        'src/github_pr_mcp_server/core.py',
        'src/github_pr_mcp_server/server.py',
        'src/github_pr_mcp_server/cli.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少必要文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # 构建包
    if not run_command("python -m build", "构建 Python 包"):
        return False
    
    return True


def test_package():
    """测试包"""
    print("🧪 测试包...")
    
    # 检查构建的文件
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist 目录不存在")
        return False
    
    wheel_files = list(dist_dir.glob('*.whl'))
    if not wheel_files:
        print("❌ 没有找到 wheel 文件")
        return False
    
    print(f"✅ 找到 {len(wheel_files)} 个 wheel 文件")
    for wheel_file in wheel_files:
        print(f"   - {wheel_file.name}")
    
    return True


def publish_to_pypi():
    """Publish to PyPI"""
    print("🚀 Publishing to PyPI...")
    
    # Set environment variables to fix Windows encoding issues
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONLEGACYWINDOWSSTDIO'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    
    test_mode = os.getenv('TEST_PYPI', 'false').lower() == 'true'
    
    if test_mode:
        print("📝 Publishing to TestPyPI (test mode)")
        command = ["python", "-m", "twine", "upload", "--repository", "testpypi", "--verbose", "dist/*"]
    else:
        print("📝 Publishing to PyPI")
        command = ["python", "-m", "twine", "upload", "--verbose", "dist/*"]
    
    try:
        # Use subprocess with proper encoding settings
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env
        )
        print("✅ Successfully published to PyPI")
        print("📦 Package has been published to PyPI")
        print("🔗 Check at https://pypi.org/project/github-pr-mcp-server/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to publish to PyPI: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def create_deployment_config():
    """创建部署配置"""
    print("📋 创建部署配置...")
    
    import toml
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        config = toml.load(f)
    
    version = config['project']['version']
    package_name = config['project']['name']
    
    mcp_config = {
        "mcpServers": {
            package_name: {
                "command": "uvx",
                "args": [f"{package_name}@latest"],
                "env": {
                    "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY",
                    "WEBHOOK_SECRET": "YOUR_WEBHOOK_SECRET",
                    "FEISHU_WEBHOOK_URL": "YOUR_FEISHU_WEBHOOK_URL",
                    "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN",
                    "WEBHOOK_PORT": "5000",
                    "GRADIO_PORT": "8080",
                    "MCP_SERVER_TYPE": "gradio"
                }
            }
        }
    }
    
    with open('mcp_square_config.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 创建部署配置: mcp_square_config.json")
    print(f"📦 包名: {package_name}")
    print(f"🏷️ 版本: {version}")
    
    return True


def main():
    """主函数"""
    print("🚀 GitHub PR MCP Server - 构建和发布")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'clean':
            clean_build()
            return
        elif command == 'build':
            clean_build()
            build_package()
            return
        elif command == 'test':
            test_package()
            return
        elif command == 'publish':
            if build_package() and test_package():
                publish_to_pypi()
            return
        elif command == 'config':
            create_deployment_config()
            return
        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: clean, build, test, publish, config")
            return
    
    print("🔄 执行完整构建和发布流程...")
    
    clean_build()
    
    if not build_package():
        print("❌ 构建失败，停止流程")
        return
    
    if not test_package():
        print("❌ 测试失败，停止流程")
        return
    
    create_deployment_config()
    
    print("\n" + "=" * 50)
    print("📋 构建完成！")
    print("💡 下一步:")
    print("   1. 检查 dist/ 目录中的文件")
    print("   2. 运行: python build_and_publish.py publish")
    print("   3. 将 mcp_square_config.json 复制到 MCP 广场")
    print("=" * 50)


if __name__ == "__main__":
    main() 