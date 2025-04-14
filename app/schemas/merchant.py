from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .auth import UserRole, SocialPreference

class MerchantBase(BaseModel):
    """商家基础信息"""
    name: str
    description: Optional[str] = None
    address: str
    phone: str
    business_license: str
    social_preference: SocialPreference

class MerchantCreate(MerchantBase):
    """创建商家请求"""
    pass

class MerchantUpdate(MerchantBase):
    """更新商家请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    business_license: Optional[str] = None
    social_preference: Optional[SocialPreference] = None

class MerchantResponse(MerchantBase):
    """商家响应"""
    id: int
    user_id: int
    status: str  # pending, approved, rejected
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MerchantApproval(BaseModel):
    """商家审批请求"""
    approved: bool
    reason: Optional[str] = None 