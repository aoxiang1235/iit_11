from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from schemas.auth import UserRole

# JWT配置
SECRET_KEY = "your-secret-key"  # JWT签名密钥，在生产环境中应该使用环境变量
ALGORITHM = "HS256"            # JWT签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期时间（分钟）

# 密码加密上下文，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2密码Bearer认证方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: 加密后的密码
    :return: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    获取密码的哈希值
    :param password: 明文密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)

def authenticate_user(db: Session, account: str, password: str) -> Optional[User]:
    """
    验证用户
    :param db: 数据库会话
    :param account: 用户账号
    :param password: 用户密码
    :return: 验证成功返回用户对象，失败返回None
    """
    # 根据账号查找用户
    user = db.query(User).filter(User.account == account).first()
    if not user:
        return None
    # 验证密码
    if not verify_password(password, user.password):
        return None
    # 检查用户是否被禁用
    if user.is_disabled:
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    :param data: 要编码的数据
    :param expires_delta: 过期时间
    :return: JWT令牌
    """
    to_encode = data.copy()
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # 生成JWT令牌
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 