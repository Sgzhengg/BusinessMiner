"""CLI 命令工具 - 用于本地操作"""
import click
from datetime import datetime
from database import SessionLocal, init_db
from app.models import RedditPost, Finding, Subscription
from app.modules.crawler import RedditCrawler
from app.modules.analyzer import AIAnalyzer
from app.modules.scheduler import start_scheduler, stop_scheduler
from config import get_settings

settings = get_settings()


@click.group()
def cli():
    """IdeaForge CLI 工具"""
    pass


@cli.command()
@click.option('--subreddit', prompt='输入 Subreddit 名称', help='如 Entrepreneur, SaaS')
@click.option('--limit', default=50, help='爬取数量')
def crawl(subreddit, limit):
    """手动爬取 Reddit 数据"""
    click.echo(f"🕷️  开始爬取 r/{subreddit}...")
    
    crawler = RedditCrawler(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_secret,
        user_agent=settings.reddit_user_agent
    )
    
    db = SessionLocal()
    count = crawler.fetch_posts(subreddit, db, limit=limit)
    click.echo(f"✓ 成功获取 {count} 条新帖子")


@cli.command()
def analyze_all():
    """分析所有未分析的帖子"""
    click.echo("🤖 开始分析未分析的帖子...")
    
    db = SessionLocal()
    analyzer = AIAnalyzer(
        api_key=settings.deepinfra_api_key,
        model=settings.deepinfra_model,
        base_url=settings.deepinfra_base_url
    )
    
    # 获取未分析的帖子
    unanalyzed = db.query(RedditPost).filter(
        ~RedditPost.id.in_(
            db.query(Finding.post_id).filter(Finding.post_id.isnot(None)).all()
        )
    ).limit(10).all()
    
    for post in unanalyzed:
        click.echo(f"分析: {post.title[:50]}...")
        analysis = analyzer.analyze_post(post.title, post.body)
        
        finding = Finding(
            post_id=post.id,
            pain_point=analysis.get("pain_point"),
            opportunity=analysis.get("opportunity"),
            target_user=analysis.get("user_type"),
            status="new"
        )
        db.add(finding)
    
    db.commit()
    click.echo(f"✓ 分析完成")


@cli.command()
def init_database():
    """初始化数据库"""
    click.echo("🗄️  初始化数据库...")
    init_db()
    click.echo("✓ 数据库初始化完成")


@cli.command()
def scheduler_start():
    """启动定时任务调度器"""
    click.echo("⏱️  启动定时任务...")
    start_scheduler()
    click.echo("✓ 定时任务已启动（按 Ctrl+C 停止）")
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\n停止定时任务...")
        stop_scheduler()


@cli.command()
@click.option('--status', default='new', help='按状态筛选')
def list_findings(status):
    """列出商机"""
    click.echo(f"📋 商机列表 (状态: {status}):")
    
    db = SessionLocal()
    findings = db.query(Finding).filter(Finding.status == status).limit(10).all()
    
    for f in findings:
        click.echo(f"\n#{f.id} - {f.pain_point[:50]}...")
        click.echo(f"   商机: {f.opportunity[:60]}...")
        click.echo(f"   状态: {f.status}")


@cli.command()
def stats():
    """查看统计信息"""
    db = SessionLocal()
    
    total_posts = db.query(RedditPost).count()
    total_findings = db.query(Finding).count()
    findings_new = db.query(Finding).filter(Finding.status == 'new').count()
    
    click.echo(f"""
📊 IdeaForge 统计信息
━━━━━━━━━━━━━━━━━━━━━━
总帖子数: {total_posts}
总商机数: {total_findings}
  - 新发现: {findings_new}
  - 研究中: {db.query(Finding).filter(Finding.status == 'researching').count()}
  - 已完成: {db.query(Finding).filter(Finding.status == 'completed').count()}
""")


if __name__ == '__main__':
    cli()
