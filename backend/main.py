"""FastAPI 主应用"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import init_db
from app.routes import router as api_router
from app.modules.scheduler import start_scheduler, stop_scheduler
from config import get_settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    logger.info("🚀 IdeaForge 启动中...")
    init_db()
    start_scheduler()
    
    yield
    
    # 关闭事件
    logger.info("🛑 IdeaForge 关闭中...")
    stop_scheduler()


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="从 Reddit 自动发现商机和用户痛点的 Web 应用",
    lifespan=lifespan
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router)

# 挂载静态文件
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
except:
    logger.warning("前端文件夹不存在或无法挂载")


@app.get("/")
def read_root():
    """根端点"""
    return {
        "message": f"欢迎使用 {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "api": "/api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
