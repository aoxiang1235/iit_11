from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from schemas.auth import UserRole, SocialPreference

class UserBase(BaseModel):
    username: str
    account: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

class UserResponse(BaseModel):
    """用户信息响应模型"""
    id: int
    username: str
    account: str
    phone_number: Optional[str] = None
    social_preference: Optional[SocialPreference] = None
    role: UserRole
    is_disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class UserDisableRequest(BaseModel):
    """用户禁用状态更新请求模型"""
    is_disabled: bool  # True 表示禁用，False 表示启用

class UserUpdateRequest(BaseModel):
    """用户信息更新请求模型"""
    phone_number: Optional[str] = None
    social_preference: Optional[SocialPreference] = None