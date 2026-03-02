# IdeaForge - 部署指南

## 前置准备

### 1. 获取 API 凭证

#### Reddit API
- 访问 https://www.reddit.com/prefs/apps
- 创建一个 "script" 类型的应用
- 记录 `Client ID`、`Client Secret`

#### OpenAI API
- 访问 https://platform.openai.com/api-keys
- 创建新的 API Key
- 记录 API Key

### 2. 依赖检查

- Docker & Docker Compose
- 或者 Python 3.9+、PostgreSQL 12+

## 部署方式

### 方式 1：Docker Compose（推荐）

#### 1. 准备环境

```bash
git clone <your-repo-url>
cd RedditMiner

# 复制并编辑环境变量
cp .env.example .env

# 编辑 .env
# REDDIT_CLIENT_ID=your_id
# REDDIT_SECRET=your_secret
# OPENAI_API_KEY=your_key
```

#### 2. 启动服务

```bash
bash run-docker.sh
```

所有服务将在后台启动：
- API: http://localhost:8000
- 数据库: localhost:5432
- Redis: localhost:6379

#### 3. 查看日志

```bash
docker-compose logs -f backend
```

#### 4. 停止服务

```bash
docker-compose down
```

### 方式 2：云服务器部署（AWS EC2 / DigitalOcean）

#### 1. SSH 连接到服务器

```bash
ssh -i your-key.pem ec2-user@your-server-ip
```

#### 2. 安装依赖

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip python3-venv postgresql postgresql-contrib redis-server docker.io docker-compose

# 启动 PostgreSQL 和 Redis
sudo systemctl start postgresql redis-server
```

#### 3. 克隆并配置

```bash
cd /home/ec2-user/
git clone <your-repo-url>
cd RedditMiner

cp .env.example .env
# 编辑 .env 文件
nano .env
```

#### 4. 使用 Systemd 服务管理

创建 `/etc/systemd/system/ideaforge.service`：

```ini
[Unit]
Description=IdeaForge API Server
After=network.target postgresql.service redis-server.service

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/RedditMiner/backend
Environment="PATH=/home/ec2-user/venv/bin"
ExecStart=/home/ec2-user/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable ideaforge
sudo systemctl start ideaforge
sudo systemctl status ideaforge
```

### 方式 3：Serverless（AWS Lambda + Supabase）

#### 部署 API 到 Railway（推荐简单方案）

1. 连接 GitHub 仓库到 Railway
2. 配置环境变量
3. 自动部署

#### 使用 Supabase PostgreSQL

1. 在 Supabase 创建项目
2. 复制连接字符串到 `DATABASE_URL`
3. 运行数据库初始化

### 方式 4：本地开发环境

```bash
cd backend
python -m venv venv
source venv/bin/activate  # 或 venv\Scripts\activate (Windows)
pip install -r requirements.txt

# 配置 .env
cp ../.env.example ../.env

# 初始化数据库
python init_db.py

# 启动应用
python main.py
```

## 生产环境配置建议

### 1. Nginx 反向代理

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. SSL 证书（Let's Encrypt）

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### 3. Uvicorn 多进程配置

```bash
# 运行多个 worker
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 监控和日志

配置 `config.py` 中的日志级别为 `INFO` 或 `WARNING`

使用服务如：
- **Sentry**：错误追踪
- **Datadog**：性能监控
- **CloudWatch**（AWS）：日志管理

### 5. 数据库备份

```bash
# 每日备份 PostgreSQL
pg_dump idea_forge > backup_$(date +%Y%m%d).sql
```

### 6. 定时任务监控

确保 APScheduler 运行正常：

```bash
curl http://localhost:8000/api/health
```

## 性能调优

### 1. 数据库优化

```sql
-- 添加索引
CREATE INDEX idx_reddit_posts_subreddit ON reddit_posts(subreddit);
CREATE INDEX idx_findings_status ON findings(status);
CREATE INDEX idx_findings_created ON findings(created_at DESC);
```

### 2. 缓存配置

在 `config.py` 中启用 Redis：

```python
redis_enabled = True
cache_ttl = 3600  # 1 小时
```

### 3. API 限流

添加速率限制（在 `routes.py`）：

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
@limiter.limit("100/minute")
def my_endpoint():
    pass
```

## 故障恢复

### 1. 数据库故障恢复

```bash
# 恢复备份
psql idea_forge < backup_20240302.sql
```

### 2. 应用崩溃恢复

使用 `systemd` 或 Docker 的 `restart_policy` 自动重启

### 3. 监控告警

配置告警规则，当服务不可用时通知

## 性能基准

| 操作 | 时间 | 说明 |
|------|------|------|
| 爬取 50 条帖子 | ~30秒 | 取决于网速和 Reddit 服务 |
| AI 分析 1 条帖子 | ~3-5秒 | 取决于 OpenAI 响应时间 |
| 获取商机列表 | <100ms | 数据库查询 + 缓存 |
| 多轮对话 | ~5-10秒 | 包含 AI 分析时间 |

## 常见问题

**Q: 如何处理 Reddit API 限流？**
A: PRAW 自动处理限流。如频繁遇到，可在 `scheduler.py` 中降低爬取频率。

**Q: OpenAI API 费用太高？**
A: 
- 使用 GPT-3.5-turbo 替代 GPT-4
- 启用结果缓存
- 限制分析频率

**Q: 如何备份重要数据？**
A: 使用 `pg_dump` 定期备份 PostgreSQL

**Q: 能否部署到多个服务器？**
A: 可以，使用 Kubernetes 或 Docker Swarm 编排多个实例

## 监控检查清单

- [ ] 定时任务是否运行
- [ ] 数据库磁盘空间充足
- [ ] 日志文件大小正常
- [ ] API 响应时间正常
- [ ] Redis 缓存命中率高
- [ ] 错误率低于阈值

## 支持和反馈

- 📧 Email: support@ideaforge.dev
- 🐛 Issue: https://github.com/your-repo/issues
- 💬 Discussions: https://github.com/your-repo/discussions
