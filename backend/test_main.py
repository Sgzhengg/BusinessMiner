"""测试用例示例"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# 添加后端路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from database import Base, get_db
from app.models import RedditPost, Finding

# 使用内存 SQLite 数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAPI:
    """API 测试用例"""
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_list_findings_empty(self):
        """测试获取空商机列表"""
        response = client.get("/api/findings")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_root_endpoint(self):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestCrawler:
    """爬虫功能测试"""
    
    def test_crawler_import(self):
        """测试爬虫模块是否可导入"""
        from app.modules.crawler import RedditCrawler
        assert RedditCrawler is not None
    
    def test_crawler_init(self):
        """测试爬虫初始化"""
        from app.modules.crawler import RedditCrawler
        crawler = RedditCrawler(
            client_id="test",
            client_secret="test",
            user_agent="test"
        )
        assert crawler.reddit is not None


class TestAnalyzer:
    """AI 分析模块测试"""
    
    def test_analyzer_import(self):
        """测试分析器模块是否可导入"""
        from app.modules.analyzer import AIAnalyzer
        assert AIAnalyzer is not None
    
    def test_analyzer_init(self):
        """测试分析器初始化"""
        from app.modules.analyzer import AIAnalyzer
        analyzer = AIAnalyzer(api_key="sk-test")
        assert analyzer.api_key is not None
        assert analyzer.model == "gpt-3.5-turbo"


class TestModels:
    """数据模型测试"""
    
    def test_reddit_post_model(self):
        """测试 RedditPost 模型"""
        from datetime import datetime
        db = TestingSessionLocal()
        
        post = RedditPost(
            id="test_id",
            subreddit="test",
            title="Test Post",
            body="Test Body",
            author="test_user",
            url="http://example.com",
            created_at=datetime.utcnow()
        )
        
        db.add(post)
        db.commit()
        
        retrieved = db.query(RedditPost).filter(RedditPost.id == "test_id").first()
        assert retrieved is not None
        assert retrieved.title == "Test Post"
        
        db.close()
    
    def test_finding_model(self):
        """测试 Finding 模型"""
        db = TestingSessionLocal()
        
        finding = Finding(
            pain_point="Sample Pain Point",
            opportunity="Sample Opportunity",
            target_user="Sample User",
            status="new"
        )
        
        db.add(finding)
        db.commit()
        
        retrieved = db.query(Finding).filter(Finding.id == finding.id).first()
        assert retrieved is not None
        assert retrieved.pain_point == "Sample Pain Point"
        
        db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
