# DeepInfra API 集成指南

本项目已配置为使用 **DeepInfra API** 调用 LLM 模型，而不是 OpenAI API。

## 🚀 快速开始

### 1. 获取 DeepInfra API Key

1. 访问 [DeepInfra](https://deepinfra.com/)
2. 注册账号或登录
3. 进入 [API Keys](https://deepinfra.com/account/keys) 页面
4. 复制你的 API Key

### 2. 配置环境变量

编辑 `.env` 文件：

```env
# DeepInfra 配置
DEEPINFRA_API_KEY=your_deepinfra_api_key_here
DEEPINFRA_MODEL=deepseek-ai/deepseek-r1-distill-llama-70b
```

### 3. 支持的模型

DeepInfra 提供多个高性能模型，推荐以下几种：

#### 开源模型（推荐）

| 模型 | ID | 说明 |
|------|----|----|
| **DeepSeek R1 Distill 70B** | `deepseek-ai/deepseek-r1-distill-llama-70b` | 推理能力强，成本低 |
| **Qwen 2.5 72B** | `Qwen/Qwen2.5-72B-Instruct` | 中文支持好，性价比高 |
| **Llama 3.1 70B** | `meta-llama/Llama-3.1-70B-Instruct` | 通用能力强 |
| **Mistral Large** | `mistralai/Mistral-Large` | 速度快，成本低 |

#### 专有模型

| 模型 | ID | 说明 |
|------|----|----|
| Claude 3.5 Sonnet | `mistralai/claude-3.5-sonnet` | 需要 Claude API Key |

### 4. 切换模型

编辑 `.env` 中的 `DEEPINFRA_MODEL` 参数，例如：

```env
# 使用 Qwen 2.5
DEEPINFRA_MODEL=Qwen/Qwen2.5-72B-Instruct

# 使用 Llama 3.1
DEEPINFRA_MODEL=meta-llama/Llama-3.1-70B-Instruct
```

## 📊 API 价格对比

DeepInfra 通常比 OpenAI 便宜 70-90%：

| 模型 | DeepInfra | OpenAI |
|------|-----------|--------|
| 高端模型 | $0.27/M tokens | $15/M tokens |
| 中等模型 | $0.05-0.1/M tokens | - |
| 开源模型 | $0.04-0.15/M tokens | - |

## 🔧 代码中的使用

### analyzer.py

```python
from app.modules.analyzer import AIAnalyzer
from config import get_settings

settings = get_settings()

# 初始化分析器
analyzer = AIAnalyzer(
    api_key=settings.deepinfra_api_key,
    model=settings.deepinfra_model,
    base_url=settings.deepinfra_base_url
)

# 分析帖子
result = analyzer.analyze_post(title, body)
# {
#   "pain_point": "...",
#   "opportunity": "...",
#   "user_type": "..."
# }

# 生成解决方案
solutions = analyzer.generate_solutions(
    pain_point="...",
    opportunity="...",
    user_type="..."
)

# 深度研究
research = analyzer.deep_research(
    question="这个痛点有没有已经被解决的案例？",
    context="..."
)
```

## 📈 性能优化建议

### 1. 缓存结果

避免重复调用相同输入：

```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_analyze(text_hash: str):
    return analyzer.analyze_post(...)
```

### 2. 批量处理

使用异步处理提高吞吐量：

```python
import asyncio

async def analyze_batch(posts):
    tasks = [asyncio.to_thread(analyzer.analyze_post, p.title, p.body) 
             for p in posts]
    return await asyncio.gather(*tasks)
```

### 3. 选择合适的模型

- **快速响应**：使用 Mistral 或 smaller models
- **高质量分析**：使用 DeepSeek-R1 或 Claude
- **成本优化**：使用开源模型

## ⚠️ 限制和注意事项

### 请求限制

- **速率限制**：取决于你的计划
- **超时**：30秒（可能根据模型调整）
- **请求大小**：token 限制根据模型而定

### 错误处理

```python
try:
    result = analyzer.analyze_post(title, body)
except Exception as e:
    logger.error(f"分析失败: {e}")
    # 降级到备选方案
```

## 🆘 故障排查

### 1. 认证错误

```
AuthenticationError: Incorrect API Key provided
```

**解决方案**：
- 检查 `DEEPINFRA_API_KEY` 是否正确
- 确保 API Key 未过期
- 在 [DeepInfra](https://deepinfra.com/account/keys) 重新生成

### 2. 模型不可用

```
Error: Model not found
```

**解决方案**：
- 检查模型名称是否正确
- 访问 [DeepInfra Models](https://deepinfra.com/models) 查看可用模型列表

### 3. 超额限额

```
Error: Rate limit exceeded
```

**解决方案**：
- 升级你的 DeepInfra 计划
- 实现更好的缓存策略
- 减少请求频率

### 4. 响应解析错误

```
JSON 解析失败
```

**解决方案**：
- 调整 prompt 确保返回有效 JSON
- 使用不同的模型重试
- 检查 token 限制

## 💡 最佳实践

1. **始终使用环境变量**
   ```env
   DEEPINFRA_API_KEY=...
   DEEPINFRA_MODEL=...
   ```

2. **监控成本**
   - 记录所有 API 调用
   - 定期检查 DeepInfra 账单

3. **实现重试机制**
   ```python
   from tenacity import retry, stop_after_attempt
   
   @retry(stop=stop_after_attempt(3))
   def call_api(...):
       ...
   ```

4. **使用日志**
   ```python
   logger.info(f"调用模型: {self.model}")
   logger.debug(f"响应: {response}")
   ```

## 🔗 相关资源

- [DeepInfra 官网](https://deepinfra.com/)
- [API 文档](https://deepinfra.com/docs)
- [模型列表](https://deepinfra.com/models)
- [定价页面](https://deepinfra.com/pricing)
- [OpenAI 兼容 API](https://deepinfra.com/docs/openai)

## 📝 更新日志

### 版本 0.1.0（当前）
- ✅ 集成 DeepInfra API
- ✅ 支持多个模型
- ✅ 完整的错误处理
- ✅ 成本优化建议

---

**提示**：如果你想在本地部署模型，参考 [本地模型部署指南](./LOCAL_MODELS.md)
