from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from schemas.auth import UserRole, SocialPreference

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
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