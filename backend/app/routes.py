"""FastAPI 路由 - API 端点"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.models import Finding, RedditPost, ChatSession, ChatMessage
from app.schemas import FindingResponse, FindingUpdate, ChatSessionResponse, ChatMessageResponse, ChatMessageCreate
from app.modules.analyzer import AIAnalyzer
from config import get_settings

router = APIRouter(prefix="/api", tags=["findings"])
settings = get_settings()
analyzer = AIAnalyzer(
    api_key=settings.deepinfra_api_key,
    model=settings.deepinfra_model,
    base_url=settings.deepinfra_base_url
)


# ============ Findings 端点 ============
@router.get("/findings", response_model=List[FindingResponse])
def list_findings(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """获取商机列表"""
    query = db.query(Finding)
    if status:
        query = query.filter(Finding.status == status)
    
    findings = query.offset(skip).limit(limit).all()
    return findings


@router.get("/findings/{finding_id}", response_model=FindingResponse)
def get_finding(finding_id: int, db: Session = Depends(get_db)):
    """获取单个商机详情"""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding


@router.patch("/findings/{finding_id}", response_model=FindingResponse)
def update_finding(
    finding_id: int,
    data: FindingUpdate,
    db: Session = Depends(get_db)
):
    """更新商机信息"""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(finding, field, value)
    
    db.commit()
    db.refresh(finding)
    return finding


@router.post("/findings/{finding_id}/generate-solutions")
def generate_solutions(finding_id: int, db: Session = Depends(get_db)):
    """生成解决方案建议"""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    solutions = analyzer.generate_solutions(
        finding.pain_point,
        finding.opportunity,
        finding.target_user or ""
    )
    
    finding.potential_solutions = solutions.get("solutions", [])
    finding.action_steps = solutions.get("action_steps", [])
    db.commit()
    
    return {
        "status": "success",
        "solutions": solutions
    }


# ============ Reddit Posts 端点 ============
@router.get("/posts", response_model=List[dict])
def list_posts(
    subreddit: str = Query(None),
    skip: int = Query(0),
    limit: int = Query(20),
    db: Session = Depends(get_db)
):
    """获取 Reddit 帖子列表"""
    query = db.query(RedditPost)
    if subreddit:
        query = query.filter(RedditPost.subreddit == subreddit)
    
    posts = query.order_by(RedditPost.created_at.desc()).offset(skip).limit(limit).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "subreddit": p.subreddit,
            "score": p.score,
            "comments": p.num_comments,
            "created_at": p.created_at
        }
        for p in posts
    ]


# ============ Chat 对话端点 ============
@router.post("/findings/{finding_id}/chat", response_model=ChatSessionResponse)
def start_chat_session(
    finding_id: int,
    title: str = "Deep Research",
    db: Session = Depends(get_db)
):
    """启动对话会话"""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    session = ChatSession(
        finding_id=finding_id,
        title=title,
        context={
            "pain_point": finding.pain_point,
            "opportunity": finding.opportunity
        }
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.post("/chat/{session_id}/message", response_model=ChatMessageResponse)
def send_message(
    session_id: int,
    message: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """发送消息并获取 AI 响应"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # 存储用户消息
    user_msg = ChatMessage(session_id=session_id, role="user", content=message.content)
    db.add(user_msg)
    db.commit()
    
    # 生成 AI 响应
    context = f"痛点: {session.context['pain_point']}\n商机: {session.context['opportunity']}"
    ai_response = analyzer.deep_research(message.content, context)
    
    # 存储 AI 消息
    ai_msg = ChatMessage(session_id=session_id, role="assistant", content=ai_response)
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)
    
    return ai_msg


@router.get("/chat/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_chat_messages(session_id: int, db: Session = Depends(get_db)):
    """获取对话历史"""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    return messages


# ============ 健康检查 ============
@router.get("/health")
def health_check():
    """健康检查端点"""
    return {"status": "ok", "service": "BusinessMiner API"}


# ============ 统计数据 ============
@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取统计数据"""
    total_findings = db.query(Finding).count()
    new_findings = db.query(Finding).filter(Finding.status == 'new').count()
    researching_findings = db.query(Finding).filter(Finding.status == 'researching').count()
    completed_findings = db.query(Finding).filter(Finding.status == 'completed').count()

    total_posts = db.query(RedditPost).count()

    return {
        "total": total_findings,
        "new": new_findings,
        "researching": researching_findings,
        "completed": completed_findings,
        "total_posts": total_posts
    }
