import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache

# 加载 .env 文件
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    # 如果 .env 不存在，也尝试从当前目录加载
    load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/businessminer.db")
    
    # Reddit API
    reddit_client_id: str = os.getenv("REDDIT_CLIENT_ID", "")
    reddit_secret: str = os.getenv("REDDIT_SECRET", "")
    reddit_user_agent: str = "idea-forge-bot/0.1 by Sgzhengg"
    
    # DeepInfra API
    deepinfra_api_key: str = os.getenv("DEEPINFRA_API_KEY", "")
    deepinfra_model: str = os.getenv("DEEPINFRA_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo")
    deepinfra_base_url: str = "https://api.deepinfra.com/v1"
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 应用配置
    env: str = os.getenv("ENV", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    app_name: str = os.getenv("APP_NAME", "IdeaForge")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    
    # 邮件配置
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    
    # Slack 配置
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
