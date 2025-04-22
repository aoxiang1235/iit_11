from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SocialPreference(str, Enum):
    """
    社交偏好枚举类
    定义用户可选的社交偏好类型
    """
    LIVELY = "Lively"      # 活跃型
    QUIET = "Quiet"        # 安静型
    BALANCED = "Balanced"  # 平衡型
    NONE = "None"          # 未设置

class UserRole(str, Enum):
    """
    用户角色枚举类
    定义系统中的用户角色类型
    """
    NORMAL = "normal"           # 普通用户
    ADMINISTRATOR = "administrator"  # 管理员
    MERCHANTS = "Merchants"     # 商户

class LoginRequest(BaseModel):
    """
    登录请求模型
    用于验证用户登录信息
    """
    account: str      # 登录账号
    password: str     # 登录密码

class LoginResponse(BaseModel):
    """
    登录响应模型
    返回登录成功后的用户信息和访问令牌
    """
    access_token: str     # JWT访问令牌
    token_type: str       # 令牌类型，固定为"bearer"
    username: str         # 用户名
    account: str          # 登录账号
    role: UserRole        # 用户角色
    social_preference: Optional[SocialPreference] = None  # 社交偏好，可选

class RegisterRequest(BaseModel):
    """
    注册请求模型
    用于创建新用户
    """
    username: str         # 用户名
    account: str          # 登录账号
    password: str         # 登录密码
    phone_number: Optional[str] = None           # 电话号码，可选
    social_preference: Optional[SocialPreference] = None  # 社交偏好，可选 