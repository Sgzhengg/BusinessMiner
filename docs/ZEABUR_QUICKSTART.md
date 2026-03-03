# Zeabur 快速部署指南

5分钟将 BusinessMiner 部署到 Zeabur。

## 第一步：准备代码

```bash
# 确保代码已推送到 GitHub
git add .
git commit -m "Ready for Zeabur deployment"
git push origin main
```

## 第二步：在 Zeabur 创建项目

1. 访问 [Zeabur](https://zeabur.com) 并登录
2. 点击 **New Project**
3. 选择 **Deploy from GitHub**
4. 授权并选择你的 BusinessMiner 仓库

## 第三步：添加 PostgreSQL

1. 在项目中点击 **Add Service**
2. 选择 **Marketplace** → **PostgreSQL**
3. 版本选择 **15**，点击 **Deploy**

## 第四步：添加后端服务

1. 点击 **Add Service**
2. 选择 **Git**
3. 选择你的仓库
4. 配置如下：
   - **Name**: `redditminer-api`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Working Directory**: `backend`

5. 添加环境变量：

```bash
DATABASE_URL=postgresql://postgres:[密码]@redditminer-db:5432/postgres
REDDIT_CLIENT_ID=[你的Reddit Client ID]
REDDIT_SECRET=[你的Reddit Secret]
DEEPINFRA_API_KEY=[你的DeepInfra API Key]
DEPPINFRA_MODEL=microsoft/WizardLM-2-8x22B
DEEPINFRA_BASE_URL=https://api.deepinfra.com/v1/openai
```

> 💡 提示：数据库密码在 PostgreSQL 服务详情中可以找到

## 第五步：初始化数据库

1. 进入后端服务的 **Terminal**
2. 运行：
   ```bash
   python init_db.py
   ```

## 第六步：访问应用

部署完成后，Zeabur 会提供访问 URL：

```
https://your-project.zeabur.app
```

访问以下地址：
- 🌐 **前端界面**: `https://your-project.zeabur.app/stitch-designs/`
- 📚 **API 文档**: `https://your-project.zeabur.app/docs`
- ❤️ **健康检查**: `https://your-project.zeabur.app/api/health`

## 🔧 绑定自定义域名（可选）

1. 在项目设置中选择 **Domains**
2. 添加你的域名
3. 按照提示配置 DNS：
   - 类型: `CNAME`
   - 名称: `www`
   - 值: `your-project.zeabur.app`

## 📊 监控和管理

### 查看日志
进入服务详情 → **Logs** 标签

### 查看资源使用
在项目首页可以看到 CPU、内存使用情况

### 重新部署
点击服务右上角的 **Redeploy** 按钮

## 🐛 常见问题

**Q: 服务启动失败**
A: 检查环境变量是否正确配置，特别是 `DATABASE_URL`

**Q: 数据库连接失败**
A: 确认 PostgreSQL 服务正在运行，密码正确

**Q: API 请求跨域错误**
A: 检查 `main.py` 中的 CORS 配置

**Q: 前端页面无法加载**
A: 确认 `frontend` 文件夹存在，静态文件路径正确

## 💰 成本说明

Zeabur 免费套餐包括：
- ✅ 每月 $5 免费额度
- ✅ 512MB RAM
- ✅ 0.5 CPU 核心
- ✅ 5GB 存储

对于开发和测试足够使用。

## 📚 更多信息

- 详细部署指南：[ZEABUR_DEPLOYMENT.md](ZEABUR_DEPLOYMENT.md)
- 部署检查清单：[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- Zeabur 官方文档：https://zeabur.com/docs

---

**有问题？** 查看 [常见问题](../README.md#-故障排查) 或提交 Issue
