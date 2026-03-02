"""数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    subscriptions = relationship("Subscription", back_populates="user")
    findings = relationship("Finding", back_populates="user")


class Subscription(Base):
    """用户订阅配置"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subreddit = Column(String)  # 例如 "Entrepreneur", "SaaS"
    keywords = Column(JSON)  # 感兴趣的关键词列表
    enabled = Column(Boolean, default=True)
    notification_email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")


class RedditPost(Base):
    """Reddit 帖子"""
    __tablename__ = "reddit_posts"
    
    id = Column(String, primary_key=True, index=True)
    subreddit = Column(String, index=True)
    title = Column(String)
    body = Column(Text)
    author = Column(String)
    url = Column(String)
    score = Column(Integer, default=0)
    num_comments = Column(Integer, default=0)
    created_at = Column(DateTime, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    findings = relationship("Finding", back_populates="post")


class Finding(Base):
    """商机发现"""
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(String, ForeignKey("reddit_posts.id"))
    pain_point = Column(Text)  # 识别的痛点
    opportunity = Column(Text)  # 对应的商机
    target_user = Column(Text, nullable=True)  # 目标用户画像
    potential_solutions = Column(JSON, nullable=True)  # 潜在解决方案列表
    action_steps = Column(JSON, nullable=True)  # 第一步行动建议
    references = Column(JSON, nullable=True)  # 参考案例
    status = Column(String, default="new")  # new, researching, completed
    research_notes = Column(Text, nullable=True)  # 深度研究笔记
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="findings")
    post = relationship("RedditPost", back_populates="findings")
    chat_sessions = relationship("ChatSession", back_populates="finding")


class ChatSession(Base):
    """多轮对话会话"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"))
    title = Column(String)
    context = Column(JSON)  # 对话上下文
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    finding = relationship("Finding", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    """对话消息"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String)  # "user" 或 "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")
