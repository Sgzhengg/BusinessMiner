"""爬虫模块 - 从 Reddit 抓取数据"""
import os
import praw
import asyncpraw
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import RedditPost

logger = logging.getLogger(__name__)


class RedditCrawler:
    """Reddit 爬虫 - 使用同步 API"""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    
    def fetch_posts(self, subreddit_name: str, db: Session, limit: int = 50, time_filter: str = "day"):
        """从指定 Subreddit 获取新帖子"""
        try:
            sub = self.reddit.subreddit(subreddit_name)
            count = 0
            
            for post in sub.new(limit=limit):
                # 检查是否已存在
                existing = db.query(RedditPost).filter(RedditPost.id == post.id).first()
                if existing:
                    continue
                
                # 创建新记录
                post_obj = RedditPost(
                    id=post.id,
                    subreddit=subreddit_name,
                    title=post.title,
                    body=post.selftext,
                    author=post.author.name if post.author else "[deleted]",
                    url=post.url,
                    score=post.score,
                    num_comments=post.num_comments,
                    created_at=datetime.utcfromtimestamp(post.created_utc),
                )
                db.add(post_obj)
                count += 1
            
            db.commit()
            logger.info(f"[{subreddit_name}] 成功获取 {count} 条新帖子")
            return count
        except Exception as e:
            logger.error(f"获取 {subreddit_name} 帖子失败: {str(e)}")
            db.rollback()
            return 0
    
    def fetch_comments(self, post_id: str, db: Session, limit: int = 20):
        """获取指定帖子的评论（可选）"""
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)
            comments = []
            
            for i, comment in enumerate(submission.comments[:limit]):
                comments.append({
                    "author": comment.author.name if comment.author else "[deleted]",
                    "score": comment.score,
                    "text": comment.body
                })
            
            logger.info(f"获取帖子 {post_id} 的 {len(comments)} 条评论")
            return comments
        except Exception as e:
            logger.error(f"获取评论失败: {str(e)}")
            return []


async def fetch_posts_async(client_id: str, client_secret: str, user_agent: str, subreddit: str, db: Session, limit: int = 50):
    """异步版本（进阶用）"""
    async with asyncpraw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    ) as reddit:
        sub = await reddit.subreddit(subreddit)
        async for post in sub.new(limit=limit):
            # 这里可以执行异步操作
            pass
