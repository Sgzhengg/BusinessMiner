# 部署前检查清单

在部署到 Zeabur 之前，请确认以下事项已完成：

## ✅ 代码检查

- [ ] 所有代码已提交到 Git 仓库
- [ ] 没有 `.env` 文件被提交（包含敏感信息）
- [ ] `.gitignore` 已正确配置
- [ ] Dockerfile 可以正常构建
- [ ] requirements.txt 包含所有依赖

## ✅ 环境变量准备

准备以下环境变量的值：

- [ ] `REDDIT_CLIENT_ID` - Reddit API 客户端 ID
- [ ] `REDDIT_SECRET` - Reddit API 密钥
- [ ] `DEEPINFRA_API_KEY` - DeepInfra API 密钥
- [ ] `POSTGRES_PASSWORD` - 数据库密码（生成一个强密码）

## ✅ 后端配置

- [ ] CORS 配置正确（`main.py`）
- [ ] 静态文件挂载正确
- [ ] 数据库初始化脚本准备（`init_db.py`）
- [ ] 健康检查端点可用（`/api/health`）
- [ ] 统计 API 端点可用（`/api/stats`）

## ✅ 前端配置

- [ ] 设备 ID 识别机制已实现（`js/device.js`）
- [ ] API 对接已完成（`js/app.js`）
- [ ] 所有页面可以正常加载
- [ ] 页面跳转功能正常
- [ ] 错误处理已实现

## ✅ 功能测试

### 本地测试

- [ ] 后端服务可以正常启动
- [ ] 可以访问 `http://localhost:8000/api/health`
- [ ] 可以访问 `http://localhost:8000/docs`（API 文档）
- [ ] 前端页面可以正常显示
- [ ] 商机列表可以正常加载
- [ ] 点击商机可以跳转到详情页
- [ ] 生成解决方案功能正常
- [ ] 深度研究对话功能正常

### API 测试

使用 curl 或 Postman 测试：

```bash
# 健康检查
curl http://localhost:8000/api/health

# 获取统计数据
curl http://localhost:8000/api/stats

# 获取商机列表
curl http://localhost:8000/api/findings?limit=5

# 获取单个商机
curl http://localhost:8000/api/findings/1
```

## ✅ 数据库测试

- [ ] 数据库表创建成功
- [ ] 可以插入测试数据
- [ ] 可以查询数据
- [ ] 定时任务可以正常执行

## ✅ 性能优化

- [ ] 图片资源已优化
- [ ] CDN 资源加载正常（Tailwind CSS, Fonts）
- [ ] 没有明显的内存泄漏
- [ ] 响应时间合理（< 2秒）

## ✅ 安全检查

- [ ] 没有 API 密钥硬编码在代码中
- [ ] 敏感信息已从 `.env.example` 移除
- [ ] CORS 配置不会过度开放（生产环境）
- [ ] 错误消息不会泄露敏感信息

## ✅ 日志配置

- [ ] 日志级别设置合理
- [ ] 重要操作有日志记录
- [ ] 错误日志包含足够的调试信息

## ✅ 部署配置

- [ ] Dockerfile 可以正常构建
- [ ] docker-compose.yml 配置正确
- [ ] Zeabur 部署文档已阅读
- [ ] 了解如何在 Zeabur 配置环境变量

## 🚀 部署步骤

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Zeabur deployment"
   git push origin main
   ```

2. **在 Zeabur 创建项目**
   - 登录 Zeabur
   - 创建新项目
   - 连接 GitHub 仓库

3. **配置服务**
   - 添加 PostgreSQL 服务
   - 添加 API 服务（Git 部署）
   - 配置环境变量

4. **初始化数据库**
   - 进入服务终端
   - 运行 `python init_db.py`

5. **测试部署**
   - 访问健康检查端点
   - 访问前端页面
   - 测试主要功能

6. **配置域名（可选）**
   - 在 Zeabur 添加自定义域名
   - 配置 DNS 记录

## 📝 部署后验证

- [ ] 应用可以正常访问
- [ ] API 文档可以打开
- [ ] 可以创建新的商机发现
- [ ] 深度研究对话功能正常
- [ ] 统计数据正确显示
- [ ] 没有控制台错误
- [ ] 日志输出正常

## 🔧 常见问题

### 构建失败

- 检查 requirements.txt 是否完整
- 确认 Python 版本兼容
- 查看构建日志

### 运行时错误

- 检查环境变量是否完整
- 查看运行日志
- 确认数据库连接正常

### 前端无法加载

- 确认静态文件路径正确
- 检查浏览器控制台错误
- 清除浏览器缓存

---

**完成所有检查后，即可开始部署！** 🎉
