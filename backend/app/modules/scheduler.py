"""定时任务调度器 - 使用 APScheduler"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from database import SessionLocal
from app.modules.crawler import RedditCrawler
from app.modules.analyzer import AIAnalyzer
from app.models import RedditPost, Finding
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# 创建调度器实例
scheduler = BackgroundScheduler()


def crawl_and_analyze_job(subreddit: str):
    """
    定时任务：抓取 Reddit 帖子并进行 AI 分析
    """
    try:
        logger.info(f"开始爬取 {subreddit} subreddit...")
        
        # 初始化爬虫和分析器
        crawler = RedditCrawler(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_secret,
            user_agent=settings.reddit_user_agent
        )
        analyzer = AIAnalyzer(
            api_key=settings.deepinfra_api_key,
            model=settings.deepinfra_model,
            base_url=settings.deepinfra_base_url
        )
        
        # 获取数据库会话
        db = SessionLocal()
        
        # 爬取帖子
        crawler.fetch_posts(subreddit, db, limit=10)
        
        # 分析新帖子
        recent_posts = db.query(RedditPost).filter(
            RedditPost.subreddit == subreddit,
            RedditPost.id.notin_(
                db.query(Finding.post_id).filter(Finding.post_id.isnot(None)).all()
            )
        ).all()
        
        for post in recent_posts:
            logger.info(f"分析帖子: {post.title[:50]}...")
            analysis = analyzer.analyze_post(post.title, post.body)
            
            # 保存分析结果
            finding = Finding(
                post_id=post.id,
                pain_point=analysis.get("pain_point", ""),
                opportunity=analysis.get("opportunity", ""),
                target_user=analysis.get("user_type", ""),
                status="new"
            )
            db.add(finding)
        
        db.commit()
        db.close()
        
        logger.info(f"✓ 完成 {subreddit} subreddit 的处理")
    except Exception as e:
        logger.error(f"定时任务失败 ({subreddit}): {str(e)}")


def start_scheduler():
    """启动调度器"""
    if scheduler.running:
        return
    
    # 每天 3:00 AM 爬取 Entrepreneur
    scheduler.add_job(
        lambda: crawl_and_analyze_job("Entrepreneur"),
        CronTrigger(hour=3, minute=0),
        id="crawl_entrepreneur",
        name="爬取 Entrepreneur subreddit"
    )
    
    # 每天 3:30 AM 爬取 SaaS
    scheduler.add_job(
        lambda: crawl_and_analyze_job("SaaS"),
        CronTrigger(hour=3, minute=30),
        id="crawl_saas",
        name="爬取 SaaS subreddit"
    )
    
    # 每天 4:00 AM 爬取 sidehustle
    scheduler.add_job(
        lambda: crawl_and_analyze_job("sidehustle"),
        CronTrigger(hour=4, minute=0),
        id="crawl_sidehustle",
        name="爬取 sidehustle subreddit"
    )
    
    scheduler.start()
    logger.info("✓ 定时任务调度器已启动")


def stop_scheduler():
    """停止调度器"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("✓ 定时任务调度器已停止")


def get_scheduler():
    """获取调度器实例"""
    return scheduler
