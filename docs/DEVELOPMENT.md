# IdeaForge - 开发指南

## 项目结构详解

### 后端代码组织

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── __init__.py              # 所有 SQLAlchemy 数据模型
│   ├── modules/
│   │   ├── crawler.py              # Reddit 爬虫（PRAW）
│   │   ├── analyzer.py             # AI 分析引擎（OpenAI）
│   │   └── scheduler.py            # APScheduler 定时任务
│   ├── routes.py                   # FastAPI 路由定义
│   └── schemas.py                  # Pydantic 验证模型
├── main.py                         # FastAPI 应用入口
├── config.py                       # 配置管理
├── database.py                     # SQLAlchemy 设置
├── cli.py                          # CLI 工具
├── init_db.py                      # 数据库初始化脚本
└── requirements.txt                # Python 依赖
```

## 开发工作流

### 1. 添加新的数据模型

编辑 `app/models/__init__.py`：

```python
class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True)
    # ... 其他字段
```

然后重新初始化数据库：

```bash
python init_db.py
```

### 2. 添加新的 API 端点

编辑 `app/routes.py`：

```python
@router.get("/new-endpoint")
def new_endpoint(db: Session = Depends(get_db)):
    # 你的逻辑
    return {}
```

### 3. 修改爬虫逻辑

编辑 `app/modules/crawler.py` 中的 `RedditCrawler` 类

### 4. 自定义 AI 分析

编辑 `app/modules/analyzer.py` 中的 `AIAnalyzer` 类

### 5. 修改定时任务

编辑 `app/modules/scheduler.py` 中的 `start_scheduler()` 函数

## 常见开发任务

### 添加新的 Subreddit 爬取

在 `scheduler.py` 的 `start_scheduler()` 中：

```python
scheduler.add_job(
    lambda: crawl_and_analyze_job("NewSubreddit"),
    CronTrigger(hour=5, minute=0),
    id="crawl_new_subreddit"
)
```

### 修改 AI 提示词

在 `analyzer.py` 的 `analyze_post()` 方法中修改 `prompt` 变量

### 添加邮件推送

在 `modules/` 下新建 `notifier.py`，并在路由中调用

### 设置 Slack 集成

在 `notifier.py` 中添加 Slack Webhook 调用

## 测试

### 手动测试爬虫

```bash
cd backend
python -c "from app.modules.crawler import RedditCrawler; from database import SessionLocal; from config import get_settings; from config import get_settings; s = get_settings(); c = RedditCrawler(s.reddit_client_id, s.reddit_secret, s.reddit_user_agent); c.fetch_posts('Entrepreneur', SessionLocal(), limit=5)"
```

### 手动测试 AI 分析

```bash
cd backend
python -c "from app.modules.analyzer import AIAnalyzer; from config import get_settings; a = AIAnalyzer(get_settings().openai_api_key); print(a.analyze_post('Sample Title', 'Sample content'))"
```

### 使用 CLI 工具

```bash
cd backend

# 爬取数据
python cli.py crawl --subreddit Entrepreneur --limit 20

# 分析数据
python cli.py analyze-all

# 查看统计
python cli.py stats

# 列举商机
python cli.py list-findings --status new
```

## 性能优化建议

1. **缓存常用查询**：使用 Redis 缓存热点数据
2. **批量操作**：在爬取或分析时使用批量插入
3. **异步处理**：使用 Celery 处理长时间任务
4. **数据库索引**：在频繁查询的字段添加索引
5. **AI 调用优化**：缓存相同输入的分析结果

## 部署前检查清单

- [ ] 所有环境变量已设置
- [ ] 数据库已初始化
- [ ] Reddit API 凭证有效
- [ ] OpenAI API 密钥有效
- [ ] SMTP 配置正确（如需要）
- [ ] 日志系统正常运行
- [ ] 定时任务已测试
- [ ] 前端资源已放置

## 故障排查

### 爬虫无法连接 Reddit

1. 检查网络连接
2. 验证 Reddit API 凭证
3. 检查速率限制
4. 查看 `debug.log`

### AI 分析失败

1. 检查 OpenAI API Key 有效性
2. 检查账户余额
3. 查看错误日志
4. 考虑降低请求频率

### 数据库连接错误

1. 确认 PostgreSQL 正在运行
2. 验证连接字符串
3. 检查防火墙/端口
4. 查看 PostgreSQL 日志

## 参考资源

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [PRAW 文档](https://praw.readthedocs.io/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [OpenAI API](https://platform.openai.com/docs/)
- [APScheduler 文档](https://apscheduler.readthedocs.io/)
