"""数据库初始化脚本"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, engine
from app.models import User, RedditPost, Finding, Subscription, ChatSession, ChatMessage

def init_database():
    """初始化所有表"""
    print("🔨 正在初始化数据库...")
    init_db()
    print("✓ 数据库初始化完成")
    
    # 打印表信息
    print("\n📋 已创建以下表:")
    for table in [User, RedditPost, Finding, Subscription, ChatSession, ChatMessage]:
        print(f"  - {table.__tablename__}")


if __name__ == "__main__":
    init_database()
