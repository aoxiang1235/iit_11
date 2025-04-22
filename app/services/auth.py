from datetime import datetime, timedelta
from typing import Optional
from jose import  jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import User

# JWT配置
SECRET_KEY = "your-secret-key"  # JWT签名密钥，在生产环境中应该使用环境变量
ALGORITHM = "HS256"            # JWT签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期时间（分钟）

# 密码加密上下文，使用bcrypt算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2密码Bearer认证方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """
    获取密码的哈希值
    :param password: 明文密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户
    :param db: 数据库会话
    :param username: 用户账号
    :param password: 用户密码
    :return: 验证成功返回用户对象
    :raises: HTTPException 当用户不存在或密码错误时
    """
    # 根据账号查找用户
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 验证密码（直接比较，不需要哈希）
    if password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
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