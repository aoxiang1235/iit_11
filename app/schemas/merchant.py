from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .auth import UserRole, SocialPreference

class MerchantBase(BaseModel):
    """商家基础信息"""
    name: str
    description: Optional[str] = None
    address: str
    business_hours: Optional[str] = None
    contact_phone: Optional[str] = None
    license_number: Optional[str] = None
    is_open: Optional[bool] = True

class MerchantCreate(MerchantBase):
    """创建商家请求"""
    pass

class MerchantUpdate(MerchantBase):
    """更新商家请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    business_hours: Optional[str] = None
    contact_phone: Optional[str] = None
    license_number: Optional[str] = None
    is_open: Optional[bool] = None

class MerchantResponse(MerchantBase):
    """商家响应"""
    id: int
    user_id: int
    is_verified: bool
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MerchantApproval(BaseModel):
    """商家审批请求"""
    is_verified: bool
    reason: Optional[str] = None 