# 📝 MCP GitHub PR 日记服务器

## 项目简介

这是一个基于 **Gradio** 和 **MCP 协议** 的 GitHub PR 监听服务器，能够自动监听 GitHub 仓库的 Pull Request 事件，使用 AI 总结 PR 内容，并将总结以日记形式发送到飞书知识库。

### 🏆 MCP&Agent挑战赛 - MCP_Agent_Challenge

本项目是 MCP&Agent挑战赛的参赛作品，展示了如何使用 MCP 协议构建智能化的开发工作流程。

## ✨ 主要功能

- 🔄 **自动监听 GitHub PR 事件**：通过 Webhook 实时接收 PR 创建和更新事件
- 🤖 **AI 智能总结**：使用 OpenAI GPT-4 自动总结 PR 内容，生成自然流畅的开发日记
- 📚 **飞书知识库集成**：将总结自动发送到飞书知识库，形成结构化的开发记录
- 🎛️ **友好的 Web 界面**：基于 Gradio 的直观配置界面，支持参数配置和状态监控
- 🔧 **MCP 服务器**：支持 MCP 协议，可与其他 MCP 工具集成

## 🏗️ 项目架构

```
MCP_PRDairy1/
├── main.py              # 主程序入口，Gradio 界面
├── github_handler.py    # GitHub Webhook 处理器
├── ai_summarizer.py     # AI 总结器
├── feishu_handler.py    # 飞书处理器
├── requirements.txt     # 项目依赖
├── env_example.txt     # 环境变量示例
└── README.md           # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装 Python 3.8+，然后克隆项目：

```bash
git clone <repository-url>
cd MCP_PRDairy1
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量示例文件并配置您的参数：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件，填入您的配置信息：

```env
# GitHub 配置
GITHUB_REPO_URL=https://github.com/your-username/your-repo
GITHUB_TOKEN=your_github_token_here
WEBHOOK_SECRET=your_webhook_secret_here

# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key_here

# 飞书配置
FEISHU_TOKEN=your_feishu_token_here
FEISHU_URL=https://open.feishu.cn/open-apis/docx/v1/spaces/your_space_id/documents
```

### 4. 启动服务
# 测试
```bash
python mcp_server_simple.py
```


```bash
python main.py
```

服务将在 `http://localhost:7860` 启动，您可以在浏览器中访问配置界面。

## 📋 配置说明

### GitHub 配置

1. **GitHub Token**：在 GitHub 设置中生成 Personal Access Token
2. **Webhook Secret**：在 GitHub 仓库设置中配置 Webhook 时设置的密钥
3. **仓库地址**：要监听的 GitHub 仓库地址

### OpenAI 配置

1. **API Key**：在 OpenAI 平台获取的 API 密钥
2. 确保有足够的 API 配额用于 GPT-4 调用

### 飞书配置

1. **API Token**：飞书开放平台的应用 Token
2. **知识库 URL**：飞书知识库的 API 端点

## 🔧 使用指南

### 1. 配置阶段

1. 在 Web 界面中填入所有必要的配置参数
2. 依次点击配置按钮测试各组件是否正常工作
3. 确认所有组件配置成功后，点击"启动 Webhook 服务器"

### 2. 运行阶段

1. 服务启动后，会显示 Webhook URL
2. 在 GitHub 仓库设置中配置 Webhook，指向该 URL
3. 当有新的 PR 创建或更新时，系统会自动处理并发送到飞书

### 3. 监控阶段

- 在"控制"标签页查看服务器状态
- 在"日志"标签页查看详细运行日志
- 在飞书知识库中查看生成的开发日记

## 📊 功能演示

### AI 总结示例

当收到 PR 事件时，AI 会生成类似以下的总结：

> "今天 张三 提交了一个 PR (#123)，主要完成了用户登录功能的优化。新增了双因子认证支持，改进了密码验证逻辑，并修复了登录页面的响应式布局问题。共修改了 5 个文件，新增 120 行，删除 45 行。"

### 飞书文档结构

生成的飞书文档包含：
- 📝 开发日记标题
- 🤖 AI 生成的总结内容
- 📋 PR 详细信息表格
- 📁 修改的文件列表

## 🔒 安全考虑

- 所有敏感信息（Token、API Key）都通过环境变量管理
- GitHub Webhook 签名验证确保请求来源的合法性
- 使用 HTTPS 进行 API 通信
- 支持可选的 Webhook Secret 验证

## 🛠️ 故障排除

### 常见问题

1. **Webhook 接收失败**
   - 检查 Webhook URL 是否正确
   - 确认 GitHub Webhook Secret 配置
   - 查看服务器日志排查问题

2. **AI 总结失败**
   - 检查 OpenAI API Key 是否有效
   - 确认 API 配额是否充足
   - 查看网络连接是否正常

3. **飞书发送失败**
   - 检查飞书 Token 是否有效
   - 确认知识库 URL 是否正确
   - 查看飞书 API 响应错误信息

### 日志查看

服务运行时会输出详细日志，包括：
- Webhook 接收事件
- AI 总结过程
- 飞书发送结果
- 错误信息

## 🚀 部署到魔搭創空間

### 1. 準備部署文件

确保项目包含以下文件：
- `main.py`
- `requirements.txt`
- `README.md`
- 所有 Python 模塊文件

### 2. 配置魔搭創空間

1. 在魔搭创空间创建新项目
2. 上传所有项目文件
3. 設置環境變數
4. 配置啟動命令：`python main.py`

### 3. 服务配置

- **服务名称**：MCP&Agent挑战赛 - GitHub PR 日记服务器
- **端口**：7860
- **MCP 服务器名称**：github_pr_dairy_server

## 🤝 貢獻指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

### 開發環境設置

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 發起 Pull Request

## 📄 許可證

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 🙏 致謝

- **Gradio**：提供優秀的 Web 界面框架
- **OpenAI**：提供強大的 AI 能力
- **飛書**：提供知識庫 API 支持
- **MCP 協議**：提供標準化的工具集成方案

---

**MCP&Agent挑战赛参赛作品** - 让开发工作流程更加智能化！ 🚀 