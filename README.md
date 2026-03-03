# IdeaForge 🚀

从 Reddit 自动发现商机和用户痛点的 AI 驱动型 Web 应用。

## ✨ 核心功能

- **定时自动挖掘** ⏱️：每天定时从 Reddit Subreddit 抓取新帖子和评论
- **痛点智能识别** 🤖：使用 GPT API 分析帖子内容，识别商机信号
- **深度研究交互** 💬：支持多轮对话，基于新的搜索进行深度分析
- **实操方案生成** 📋：自动生成包括问题概述、目标用户、潜在解决方案的方案建议
- **推送与通知** 📧：支持邮件、Slack 推送新发现

## 🚀 快速开始

### Docker 方式（推荐）

```bash
# 克隆项目
git clone <repo-url>
cd BusinessMiner

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 Reddit 和 OpenAI 的 API Key

# 启动
bash run-docker.sh
```

### 本地方式

```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动应用
python main.py
```

应用将在 http://localhost:8000 启动

访问前端界面：
- **新版 UI（推荐）**: http://localhost:8000/stitch-designs/
- **旧版 UI**: http://localhost:8000/

## 📚 文档

- [🏃 快速开始](docs/QUICKSTART.md) - 5 分钟上手
- [☁️ Zeabur 部署](docs/ZEABUR_QUICKSTART.md) - 5分钟部署到 Zeabur
- [👨‍💻 开发指南](docs/DEVELOPMENT.md) - 项目结构和开发工作流
- [🚀 部署指南](docs/DEPLOYMENT.md) - 到云服务器和生产环境的部署
- [✅ 部署检查清单](docs/DEPLOYMENT_CHECKLIST.md) - 部署前必读

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 后端 | FastAPI + SQLAlchemy |
| 数据库 | PostgreSQL |
| 爬虫 | PRAW (Reddit API) |
| AI | OpenAI API (GPT-3.5/4) |
| 调度 | APScheduler |
| 前端 | HTML/CSS/JavaScript + Tailwind CSS |
| 前端架构 | SPA (单页应用) + Hash 路由 |
| 设计系统 | Glassmorphism (玻璃态设计) |
| 部署 | Docker + Docker Compose |

## 📂 项目结构

```
BusinessMiner/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── modules/           # 核心业务模块
│   │   ├── routes.py          # API 路由
│   │   └── schemas.py         # 数据验证
│   ├── main.py                # FastAPI 应用
│   ├── config.py              # 配置管理
│   ├── cli.py                 # CLI 工具
│   └── requirements.txt
├── frontend/                   # 前端 Web UI
│   ├── index.html             # 旧版单页面应用（备用）
│   └── stitch-designs/        # 新版 SPA 应用（推荐）
│       ├── index.html         # 主入口文件
│       ├── css/               # 样式文件
│       ├── js/                # JavaScript 文件
│       ├── pages/             # 页面组件
│       └── README.md          # 前端架构说明
├── docs/                       # 文档
├── docker-compose.yml          # Docker 配置
└── README.md                   # 本文件
```

## 🔑 环境变量

必须配置：

```env
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_SECRET=<your-reddit-secret>
OPENAI_API_KEY=<your-openai-api-key>
DATABASE_URL=postgresql://user:password@localhost:5432/idea_forge
```

详见 `.env.example`

## 🌐 API 端点

访问 http://localhost:8000/docs 查看完整 Swagger 文档

主要端点：

```
GET  /api/findings              # 获取商机列表
GET  /api/findings/{id}         # 获取商机详情
POST /api/findings/{id}/chat    # 启动深度研究对话
GET  /api/posts                 # 获取 Reddit 帖子
GET  /api/health                # 健康检查
```

## 💡 使用示例

### 获取商机列表

```bash
curl http://localhost:8000/api/findings?limit=10
```

### 生成解决方案

```bash
curl -X POST http://localhost:8000/api/findings/1/generate-solutions
```

### 启动对话会话

```bash
curl -X POST http://localhost:8000/api/findings/1/chat \
  -H "Content-Type: application/json" \
  -d '{"title":"Deep Research"}'
```

## ⚙️ 命令行工具

```bash
cd backend

# 手动爬取数据
python cli.py crawl --subreddit Entrepreneur --limit 50

# 分析未分析的帖子
python cli.py analyze-all

# 查看统计信息
python cli.py stats

# 列出商机
python cli.py list-findings --status new
```

## 🐛 故障排查

### 数据库连接失败

确保 PostgreSQL 正在运行：

```bash
sudo systemctl start postgresql
```

### Reddit API 认证失败

- 检查 REDDIT_CLIENT_ID 和 REDDIT_SECRET 是否正确
- 确认 https://www.reddit.com/prefs/apps 中的应用类型为 "script"

### OpenAI API 错误

- 验证 API Key 有效性
- 检查账户配额

## 📊 功能路线图

### MVP（已完成）✅
- Reddit 数据爬取
- AI 痛点识别
- 商机展示仪表板
- 深度研究对话
- Web UI 和 REST API

### 迭代一（进行中）
- [x] 现代化前端 UI（Stitch 设计集成）
- [ ] 用户账号系统
- [ ] 邮件/Slack 推送
- [ ] 更多 Subreddit 支持
- [ ] 高级过滤和搜索

### 迭代二（计划中）
- [ ] 本地 AI 模型部署
- [ ] 报告导出功能
- [ ] 推荐引擎
- [ ] 仪表板定制化

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License

## 📧 联系

- 💬 GitHub Issues: 报告问题或建议
- 📧 Email: contact@ideaforge.dev

---

**🎯 让发现商机变得简单！**
