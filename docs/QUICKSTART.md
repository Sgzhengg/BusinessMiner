# 项目快速开始指南

## ⏱️ 5 分钟快速启动

### 前置条件
- Python 3.9+
- PostgreSQL 正在运行
- Reddit 和 OpenAI API 凭证

### 步骤 1：克隆并配置

```bash
git clone <repo-url>
cd RedditMiner

# 复制环境文件
cp .env.example .env

# 编辑 .env，填入你的 API Key
# 使用你喜欢的编辑器打开 .env
```

### 步骤 2：安装依赖

```bash
cd backend
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate      # Windows

# 安装依赖
pip install -r requirements.txt
cd ..
```

### 步骤 3：初始化数据库

```bash
cd backend
python init_db.py
```

你应该看到类似的输出：
```
🔨 正在初始化数据库...
✓ 数据库初始化完成

📋 已创建以下表:
  - users
  - reddit_posts
  - findings
  - subscriptions
  - chat_sessions
  - chat_messages
```

### 步骤 4：启动应用

```bash
python main.py
```

你应该看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ 定时任务调度器已启动
```

### 步骤 5：访问应用

打开浏览器访问：
- **前端**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

## 🐳 Docker 快速启动（推荐）

```bash
# 进入项目目录
cd RedditMiner

# 复制环境文件
cp .env.example .env

# 编辑 .env 文件
# 然后运行：
bash run-docker.sh
```

完成！访问 http://localhost:8000

## 📝 使用指南

### 1. 查看仪表板

访问 http://localhost:8000 查看：
- 商机统计
- 最近发现
- 快速操作按钮

### 2. 手动爬取数据

**通过 Web UI:**
- 点击"立即爬取"按钮
- 输入 Subreddit 名称和数量
- 点击"开始爬取"

**通过 CLI:**
```bash
cd backend
python cli.py crawl --subreddit Entrepreneur --limit 20
```

### 3. 查看 API 文档

访问 http://localhost:8000/docs 查看完整的 Swagger 文档和实时测试

### 4. 深度研究功能

点击任何商机卡片 → 点击"深度研究"按钮 → 输入你的问题

示例问题：
- "这个痛点有没有已经被解决的案例？"
- "目标用户画像是什么？"
- "前三步应该如何执行？"

### 5. 定时任务

应用启动时，定时任务自动开始运行：
- 每天 3:00 AM：爬取 r/Entrepreneur
- 每天 3:30 AM：爬取 r/SaaS
- 每天 4:00 AM：爬取 r/sidehustle

## 🔍 常见操作

### 获取所有商机

```bash
curl http://localhost:8000/api/findings?limit=10
```

### 获取特定状态的商机

```bash
curl http://localhost:8000/api/findings?status=new&limit=5
```

### 为商机生成解决方案

```bash
curl -X POST http://localhost:8000/api/findings/1/generate-solutions
```

### 启动对话会话

```bash
curl -X POST http://localhost:8000/api/findings/1/chat \
  -H "Content-Type: application/json" \
  -d '{"title":"Research Session"}'
```

## 📊 查看统计数据

```bash
cd backend
python cli.py stats
```

输出示例：
```
📊 IdeaForge 统计信息
━━━━━━━━━━━━━━━━━━━━━━
总帖子数: 150
总商机数: 45
  - 新发现: 30
  - 研究中: 10
  - 已完成: 5
```

## 📁 项目文件说明

| 文件/文件夹 | 说明 |
|-----------|------|
| `backend/` | 后端代码 |
| `frontend/` | 前端 Web UI |
| `docs/` | 文档 |
| `docker-compose.yml` | Docker 配置 |
| `.env.example` | 环境变量模板 |
| `run.sh` | 本地启动脚本 |
| `run-docker.sh` | Docker 启动脚本 |

## ⚙️ 环境变量配置

必填项：
- `REDDIT_CLIENT_ID` - Reddit API 客户端 ID
- `REDDIT_SECRET` - Reddit API Secret
- `OPENAI_API_KEY` - OpenAI API Key
- `DATABASE_URL` - PostgreSQL 连接字符串

可选项：
- `REDIS_URL` - Redis 连接（用于缓存）
- `SMTP_SERVER` - 邮件服务器
- `SLACK_WEBHOOK_URL` - Slack 推送

## 🆘 故障排查

### 错误："无法连接到数据库"

```bash
# 检查 PostgreSQL 是否运行
sudo systemctl status postgresql

# 如果没启动
sudo systemctl start postgresql

# 创建数据库（如需要）
sudo -u postgres createdb idea_forge
```

### 错误："Reddit API 认证失败"

- [ ] 检查 `REDDIT_CLIENT_ID` 和 `REDDIT_SECRET` 是否正确
- [ ] 确认 Reddit 应用类型为 "script"
- [ ] 检查 API 访问频率是否过高

### 错误："OpenAI API Key 无效"

- [ ] 在 https://platform.openai.com/api-keys 验证 API Key
- [ ] 检查账户是否有足够的配额
- [ ] 确认 API Key 没有过期

### 应用崩溃

查看日志（Docker）：
```bash
docker-compose logs -f backend
```

或本地：
```bash
# 查看最后 100 行日志
tail -100 debug.log
```

## 📚 下一步

- 阅读 [DEVELOPMENT.md](./DEVELOPMENT.md) 了解开发指南
- 阅读 [DEPLOYMENT.md](./DEPLOYMENT.md) 了解部署方案
- 查看 API 文档 [http://localhost:8000/docs](http://localhost:8000/docs)
- 加入社区讨论和贡献

## 💡 技术栈

- **后端**: FastAPI + SQLAlchemy + PostgreSQL
- **爬虫**: PRAW (Reddit API)
- **AI**: OpenAI API (GPT-3.5/4)
- **调度**: APScheduler
- **前端**: 原生 HTML/CSS/JavaScript
- **部署**: Docker + Docker Compose

## 🎯 MVP 功能清单

✅ 定时爬取 Reddit 数据
✅ AI 智能识别痛点  
✅ 商机展示仪表板
✅ 深度研究对话
✅ 解决方案生成
✅ API 接口
✅ Web UI
⏳ 邮件/Slack 推送（下一步）
⏳ 用户账号系统（下一步）
⏳ 高级报告导出（迭代版本）

---

**祝你使用愉快！有任何问题欢迎提出 Issue！🚀**
