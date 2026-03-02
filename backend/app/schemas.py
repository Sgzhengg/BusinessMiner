"""Pydantic 数据验证模型"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ User 相关 ============
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Finding 相关 ============
class FindingCreate(BaseModel):
    pain_point: str
    opportunity: str
    target_user: Optional[str] = None


class FindingUpdate(BaseModel):
    status: Optional[str] = None
    research_notes: Optional[str] = None
    target_user: Optional[str] = None
    potential_solutions: Optional[List[Dict[str, Any]]] = None


class FindingResponse(BaseModel):
    id: int
    pain_point: str
    opportunity: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ Chat 相关 ============
class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatSessionCreate(BaseModel):
    title: str


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    is_active: bool
    created_at: datetime
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True
