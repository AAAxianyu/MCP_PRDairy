# GitHub PR MCP Server - 部署指南

## 自动化部署检测要求

根据 MCP 广场的自动化部署检测要求，本项目已完全符合以下标准：

### 1. 服务配置解析 ✅

- ✅ 服务配置字段完整
- ✅ 所有必需参数已定义
- ✅ 配置格式正确

### 2. 校验服务配置可用性 ✅

- ✅ 使用 `uvx` 命令（符合要求）
- ✅ JSON 完整性检查通过
- ✅ 无注释内容（符合要求）
- ✅ 采用第一个服务配置进行部署

### 3. 尝试部署并连接到 MCP 服务 ✅

- ✅ 包已发布到 PyPI
- ✅ 支持 `uvx` 安装
- ✅ 自动调用 `list_tools` 方法
- ✅ 成功连接验证

## 部署配置

### MCP 广场服务配置

```json
{
  "mcpServers": {
    "github-pr-mcp-server": {
      "command": "uvx",
      "args": ["github-pr-mcp-server@latest"],
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
```

### 配置说明

| 字段 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `command` | 命令类型 | ✅ | `uvx` |
| `args` | 包名参数 | ✅ | `["github-pr-mcp-server@latest"]` |
| `env.OPENAI_API_KEY` | OpenAI API 密钥 | ✅ | - |
| `env.WEBHOOK_SECRET` | GitHub Webhook 密钥 | ❌ | - |
| `env.FEISHU_WEBHOOK_URL` | 飞书 Webhook URL | ❌ | - |
| `env.GITHUB_TOKEN` | GitHub 令牌 | ❌ | - |
| `env.WEBHOOK_PORT` | Webhook 端口 | ❌ | `5000` |
| `env.GRADIO_PORT` | Gradio 端口 | ❌ | `8080` |
| `env.MCP_SERVER_TYPE` | 服务器类型 | ❌ | `gradio` |

## 部署步骤

### 1. 准备环境

确保系统已安装：
- Python 3.8+
- `uvx` 工具（可选，用于快速安装）

```bash
# 安装 uvx（推荐）
pip install uvx
```

### 2. 配置环境变量

设置必要的环境变量：

```bash
# 必需配置
export OPENAI_API_KEY="your_openai_api_key_here"

# 可选配置
export WEBHOOK_SECRET="your_github_webhook_secret"
export FEISHU_WEBHOOK_URL="your_feishu_webhook_url"
export GITHUB_TOKEN="your_github_token"
export MCP_SERVER_TYPE="gradio"  # 或 flask
export WEBHOOK_PORT="5000"
export GRADIO_PORT="8080"
```

### 3. 安装和运行

#### 方法一：使用 uvx（推荐）

```bash
# 直接运行
uvx github-pr-mcp-server@latest
```

#### 方法二：使用 pip

```bash
# 安装包
pip install github-pr-mcp-server

# 运行服务器
github-pr-mcp-server
```

#### 方法三：从源码安装

```bash
# 克隆仓库
git clone https://github.com/your-username/github-pr-mcp-server.git
cd github-pr-mcp-server

# 安装依赖
pip install -e .

# 运行服务器
python -m github_pr_mcp_server
```

### 4. 验证部署

#### 健康检查

```bash
# Gradio 服务器
curl http://localhost:8080/

# Flask 服务器
curl http://localhost:5000/health
```

#### MCP 功能测试

```bash
# 测试 MCP 端点
curl -X POST http://localhost:8080/gradio_api/mcp/sse \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

## MCP 广场部署

### 1. 创建 MCP 服务

1. 访问 [MCP 广场](https://modelscope.cn/mcp/servers/create?template=customize)
2. 选择"自定义创建"
3. 填写基础信息：
   - **英文名称**: `GitHub PR MCP Server - MCP_Agent_Challenge`
   - **中文名称**: `GitHub PR MCP Server - MCP&Agent挑战赛`
   - **来源地址**: `https://github.com/your-username/github-pr-mcp-server`
   - **托管类型**: 选择"可托管部署"

### 2. 配置服务

将以下配置复制到服务配置字段：

```json
{
  "mcpServers": {
    "github-pr-mcp-server": {
      "command": "uvx",
      "args": ["github-pr-mcp-server@latest"],
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
```

### 3. 填写 README

确保 README 包含以下三个部分：

1. **项目简介**: 描述功能、技术栈、使用场景
2. **部署指南**: 安装方法、环境配置、启动命令
3. **使用示例**: 具体的使用案例和效果展示

### 4. 提交创建

1. 点击"创建"按钮
2. 等待自动化部署检测
3. 检测通过后获得"可部署"和"hosted"标签

## 部署检测要点

### ✅ 符合要求的配置

1. **命令类型**: 使用 `uvx` 或 `npx`
2. **包名格式**: `github-pr-mcp-server@latest`
3. **环境变量**: 统一收敛到 `env` 字段
4. **JSON 格式**: 无注释，格式正确
5. **依赖管理**: 不依赖本地资源

### ✅ 功能验证

1. **list_tools 方法**: 成功响应工具列表
2. **参数验证**: 正确处理输入参数
3. **错误处理**: 友好的错误信息
4. **类型注解**: 完整的类型定义

### ✅ 安全考虑

1. **API 密钥**: 通过环境变量配置
2. **Webhook 验证**: 支持签名验证
3. **HTTPS 支持**: 生产环境建议使用
4. **访问控制**: 可配置访问限制

## 故障排除

### 常见问题

1. **部署检测失败**
   - 检查 JSON 格式是否正确
   - 确认包名是否已发布到 PyPI
   - 验证环境变量配置

2. **连接失败**
   - 检查网络连接
   - 验证端口是否被占用
   - 确认防火墙设置

3. **功能异常**
   - 检查 API 密钥是否有效
   - 验证依赖包是否正确安装
   - 查看错误日志

### 调试方法

1. **本地测试**
   ```bash
   # 本地运行测试
   python -m github_pr_mcp_server
   ```

2. **日志查看**
   ```bash
   # 查看详细日志
   MCP_SERVER_TYPE=flask python -m github_pr_mcp_server
   ```

3. **健康检查**
   ```bash
   # 检查服务状态
   curl http://localhost:5000/health
   ```

## 更新和维护

### 版本更新

1. 修改 `pyproject.toml` 中的版本号
2. 重新构建和发布包
3. 更新 MCP 广场配置

### 功能扩展

1. 添加新的 MCP 函数
2. 更新依赖包版本
3. 改进错误处理机制

### 监控和维护

1. 定期检查 API 配额
2. 监控服务性能
3. 更新安全配置

## 支持信息

- **项目地址**: https://github.com/your-username/github-pr-mcp-server
- **问题反馈**: https://github.com/your-username/github-pr-mcp-server/issues
- **文档**: https://github.com/your-username/github-pr-mcp-server#readme
- **许可证**: MIT License

---

**MCP&Agent Challenge** - 让开发工作流程更加智能化！ 🚀 