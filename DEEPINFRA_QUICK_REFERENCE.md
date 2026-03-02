# DeepInfra API 快速参考

## 📋 修改清单

✅ **配置文件**
- `.env.example` - 改用 DeepInfra 变量
- `backend/config.py` - 新增 DeepInfra 配置

✅ **核心代码**
- `backend/app/modules/analyzer.py` - 完全迁移至 DeepInfra API
- `backend/app/routes.py` - 更新 AIAnalyzer 初始化
- `backend/app/modules/scheduler.py` - 定时任务改用 DeepInfra
- `backend/cli.py` - CLI 工具改用 DeepInfra

✅ **测试工具**
- `backend/test_deepinfra.py` - 集成测试脚本
- `setup-deepinfra.sh` - 快速配置脚本

✅ **文档**
- `docs/DEEPINFRA_SETUP.md` - 完整集成指南

## 🚀 3 步快速开始

### 1️⃣ 获取 API Key
```bash
访问 https://deepinfra.com/ → 注册 → 获取 API Key
```

### 2️⃣ 配置环境
```bash
cp .env.example .env

# 编辑 .env，填入:
DEEPINFRA_API_KEY=sk_xxxxxxxxxxxx
DEEPINFRA_MODEL=deepseek-ai/deepseek-r1-distill-llama-70b
```

### 3️⃣ 运行测试验证
```bash
cd backend
python test_deepinfra.py
```

## 📊 模型选择

| 模型名称 | 模型 ID | 特点 | 成本 |
|---------|--------|------|------|
| **DeepSeek R1** | `deepseek-ai/deepseek-r1-distill-llama-70b` | 推理强 | ⭐ 最低 |
| **Qwen 2.5** | `Qwen/Qwen2.5-72B-Instruct` | 中文好 | ⭐ 低 |
| **Llama 3.1** | `meta-llama/Llama-3.1-70B-Instruct` | 通用 | ⭐⭐ 低 |
| **Mistral** | `mistralai/Mistral-Large` | 快速 | ⭐ 最低 |

## 💻 代码示例

### 分析 Reddit 帖子
```python
from app.modules.analyzer import AIAnalyzer
from config import get_settings

settings = get_settings()
analyzer = AIAnalyzer(
    api_key=settings.deepinfra_api_key,
    model=settings.deepinfra_model,
    base_url=settings.deepinfra_base_url
)

# 分析帖子
result = analyzer.analyze_post(
    title="项目管理工具太复杂了",
    body="我找不到一个简单易用的..."
)

print(result['pain_point'])      # 用户的痛点
print(result['opportunity'])    # 商机
print(result['user_type'])      # 目标用户
```

### 生成解决方案
```python
solutions = analyzer.generate_solutions(
    pain_point="项目管理复杂",
    opportunity="市场需求高",
    user_type="中小团队"
)

for sol in solutions['solutions']:
    print(f"{sol['name']} - {sol['type']}")
```

### 深度研究对话
```python
research = analyzer.deep_research(
    question="这个市场有哪些竞品？",
    context="痛点: 项目管理工具太复杂"
)

print(research)
```

## 📈 性能对比

| 指标 | OpenAI | DeepInfra |
|-----|--------|-----------|
| 成本 | $15/M tokens | $0.04-0.27/M tokens |
| 节省 | - | **70-99%** ↓ |
| 速度 | 快 | 快 |
| 支持 | 专有模型 | 开源 + 专有 |

## 🔧 故障排查

### API Key 错误
```
❌ AuthenticationError: Incorrect API Key
✅ 解决: 检查 .env 中的 DEEPINFRA_API_KEY
```

### 模型不存在
```
❌ Error: Model not found
✅ 解决: 检查模型名称或访问 https://deepinfra.com/models
```

### 速率限制
```
❌ Rate limit exceeded
✅ 解决: 升级 DeepInfra 计划或增加缓存
```

## 🧪 验证安装

### 方式 1：直接运行测试
```bash
cd backend && python test_deepinfra.py
```

### 方式 2：启动完整应用
```bash
cd backend && python main.py
# 访问 http://localhost:8000
```

### 方式 3：CLI 测试
```bash
cd backend
python cli.py crawl --subreddit Entrepreneur --limit 5
python cli.py analyze-all
```

## 📚 相关文档

- 📖 [完整 DeepInfra 指南](docs/DEEPINFRA_SETUP.md)
- 📖 [快速开始指南](docs/QUICKSTART.md)
- 📖 [开发指南](docs/DEVELOPMENT.md)
- 🔗 [DeepInfra 官网](https://deepinfra.com/)

## 💡 最佳实践

1. **监控成本**
   ```python
   # 启用日志记录
   logger.info(f"调用模型: {self.model}")
   ```

2. **实现缓存**
   ```python
   @lru_cache(maxsize=128)
   def cached_analyze(...): ...
   ```

3. **错误处理**
   ```python
   try:
       result = analyzer.analyze_post(...)
   except Exception as e:
       logger.error(f"分析失败: {e}")
   ```

4. **批量处理**
   ```python
   # 使用异步处理提高效率
   asyncio.gather(*tasks)
   ```

## 🎯 下一步

- [ ] 配置 DeepInfra API Key
- [ ] 运行 test_deepinfra.py 验证连接
- [ ] 启动应用并测试功能
- [ ] （可选）切换到其他模型
- [ ] （可选）启用缓存优化成本

---

**💰 ¡节省 70-99% 的 API 成本！**
