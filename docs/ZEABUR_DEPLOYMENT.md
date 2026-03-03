# Zeabur 部署指南

本文档说明如何将 BusinessMiner 部署到 Zeabur 平台。

## 📋 前置要求

1. Zeabur 账号（注册：https://zeabur.com）
2. GitHub 账号（用于连接代码仓库）
3. 以下 API 密钥：
   - Reddit API 凭证
   - DeepInfra API 密钥

## 🚀 部署步骤

### 1. 准备代码仓库

确保你的代码已经推送到 GitHub 仓库。

### 2. 在 Zeabur 创建项目

1. 登录 [Zeabur](https://zeabur.com)
2. 点击 "New Project"
3. 选择 "Deploy from GitHub"
4. 授权并选择你的 BusinessMiner 仓库

### 3. 配置环境变量

在项目设置中添加以下环境变量：

```bash
# 数据库配置（由 Zeabur PostgreSQL 服务提供）
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://redditminer:your_secure_password@redditminer-db:5432/redditminer

# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=BusinessMiner/1.0

# DeepInfra API
DEEPINFRA_API_KEY=your_deepinfra_api_key
DEEPINFRA_MODEL=microsoft/WizardLM-2-8x22B
DEEPINFRA_BASE_URL=https://api.deepinfra.com/v1/openai
```

### 4. 添加服务

#### 方式 A：使用 Docker Compose（推荐）

Zeabur 支持 Docker Compose，可以直接使用现有的 `docker-compose.yml`：

1. 在 Zeabur 项目中选择 "Add Service"
2. 选择 "Docker Compose"
3. 选择 `docker-compose.yml` 文件

#### 方式 B：手动添加服务

##### 4.1 添加 PostgreSQL 数据库

1. 点击 "Add Service"
2. 选择 "Marketplace"
3. 选择 "PostgreSQL"
4. 配置：
   - 名称：`redditminer-db`
   - 版本：`15`
   - 设置 Root 密码

##### 4.2 添加后端 API 服务

1. 点击 "Add Service"
2. 选择 "Git"
3. 选择你的仓库
4. 配置：
   - 名称：`redditminer-api`
   - 运行时：Python
   - 构建命令：`pip install -r requirements.txt`
   - 启动命令：`uvicorn main:app --host 0.0.0.0 --port 8000`
   - 工作目录：`backend`

##### 4.3 连接服务

在 API 服务中，添加数据库连接：

1. 进入 API 服务设置
2. 找到 "Dependencies" 或 "Environment Variables"
3. 添加数据库连接字符串：
   ```
   DATABASE_URL=postgresql://redditminer:your_password@redditminer-db:5432/redditminer
   ```

### 5. 初始化数据库

部署完成后，需要初始化数据库：

1. 在 Zeabur 控制台进入 API 服务的终端
2. 运行：
   ```bash
   cd backend
   python init_db.py
   ```

或者，你也可以在本地运行初始化脚本连接到远程数据库。

### 6. 访问应用

部署成功后，Zeabur 会提供一个公网 URL：

```
https://your-project.zeabur.app
```

访问以下地址：
- 前端：`https://your-project.zeabur.app/stitch-designs/`
- API 文档：`https://your-project.zeabur.app/docs`
- API：`https://your-project.zeabur.app/api`

## 🔧 配置优化

### 域名绑定（可选）

1. 在 Zeabur 项目设置中选择 "Domains"
2. 添加你的自定义域名
3. 按照提示配置 DNS 记录

### 持久化存储

确保数据库数据持久化：

1. 进入 PostgreSQL 服务设置
2. 找到 "Volumes" 或 "Persistent Storage"
3. 确认已启用数据持久化

### 健康检查

Zeabur 会自动监控服务健康状态。确保 API 的健康检查端点正常：

```bash
curl https://your-project.zeabur.app/api/health
```

应该返回：
```json
{"status": "ok", "service": "BusinessMiner API"}
```

## 📊 监控和日志

### 查看日志

1. 进入服务详情页
2. 点击 "Logs" 标签
3. 实时查看应用日志

### 性能监控

1. 在项目概览页查看资源使用情况
2. 关注 CPU、内存和磁盘使用率

### 定时任务

Reddit 爬虫使用 APScheduler 自动运行，在日志中可以看到：

```
INFO - 🕷️ 开始爬取 Reddit 数据...
INFO - ✓ 成功获取 50 条新帖子
INFO - 🤖 开始分析帖子...
INFO - ✓ 分析完成，发现 5 个新商机
```

## 🐛 故障排查

### 服务无法启动

1. 检查环境变量是否正确配置
2. 查看构建日志，确认依赖安装成功
3. 查看运行日志，定位具体错误

### 数据库连接失败

1. 确认 PostgreSQL 服务正在运行
2. 检查 `DATABASE_URL` 格式是否正确
3. 确认服务之间网络连通性

### API 请求失败

1. 检查 CORS 配置
2. 确认端口映射正确（默认 8000）
3. 查看日志中的具体错误信息

### 前端无法加载

1. 确认静态文件路径正确
2. 检查前端文件是否正确部署
3. 清除浏览器缓存重试

## 🔄 更新部署

### 自动部署

Zeabur 默认启用自动部署。当代码推送到主分支时，会自动重新部署。

### 手动部署

1. 进入项目或服务设置
2. 点击 "Redeploy" 按钮
3. 等待部署完成

## 💰 成本优化

### 资源配置

根据实际使用调整资源配置：

- 开发环境：最小配置即可
- 生产环境：根据流量调整
- 数据库：使用标准套餐保证稳定性

### 休眠策略

对于开发环境，可以设置自动休眠以节省成本。

## 🔐 安全建议

1. **环境变量安全**：
   - 不要在代码中硬编码密钥
   - 使用 Zeabur 的环境变量功能
   - 定期轮换 API 密钥

2. **访问控制**：
   - 启用域名访问
   - 考虑添加身份验证（如果需要）

3. **数据备份**：
   - 定期备份数据库
   - 启用 PostgreSQL 自动备份

## 📚 相关资源

- [Zeabur 官方文档](https://zeabur.com/docs)
- [Docker Compose 指南](https://docs.docker.com/compose/)
- [FastAPI 部署指南](https://fastapi.tiangolo.com/deployment/)

## 🆘 获取帮助

如果遇到问题：

1. 查看 [Zeabur 常见问题](https://zeabur.com/docs/faq)
2. 搜索项目 Issues
3. 联系技术支持

---

**祝部署顺利！** 🎉
