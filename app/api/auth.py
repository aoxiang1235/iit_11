from abc import ABC, abstractmethod
from passlib.context import CryptContext
from datetime import datetime
from jose import  jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.auth import  LoginResponse, RegisterRequest, UserRole
from models.user import User
from services.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# 创建路由器
router = APIRouter()

@router.post("/register", response_model=dict)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    :param request: 注册请求数据
    :param db: 数据库会话
    :return: 注册结果
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # 检查账号是否已存在
    if db.query(User).filter(User.account == request.account).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already registered"
        )
    
    # 创建新用户
    hashed_password = request.password
    db_user = UserFactory.create(
         username=request.username,
         account=request.account,
         password=request.password,
         phone_number=request.phone_number,
         social_preference=request.social_preference,
         role=UserRole.NORMAL
     )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully"}

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    :param form_data: 登录表单数据
    :param db: 数据库会话
    :return: 登录成功返回用户信息和访问令牌
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    # 创建访问令牌
    strategy = HashedPasswordStrategy() if user.password.startswith("$2") else PlainPasswordStrategy()
    if not PasswordContext(strategy).verify(user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 单例模式生成访问令牌 Generate access token in Singleton Pattern
    token_manager = TokenManager()
    access_token = token_manager.create_token({"sub": user.username})
    
    # 返回登录响应
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        account=user.account,
        role=user.role,
        social_preference=user.social_preference
    ) 


# 策略模式：密码验证策略接口与实现。Strategy pattern: password verification strategy interface and implementation
class PasswordStrategy(ABC):
    @abstractmethod
    def verify(self, plain_password: str, stored_password: str) -> bool:
        pass

class PlainPasswordStrategy(PasswordStrategy):
    def verify(self, plain_password: str, stored_password: str) -> bool:
        return plain_password == stored_password

class HashedPasswordStrategy(PasswordStrategy):
    def verify(self, plain_password: str, stored_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, stored_password)

class PasswordContext:
    def __init__(self, strategy: PasswordStrategy):
        self._strategy = strategy
    def verify(self, plain_password: str, stored_password: str) -> bool:
        return self._strategy.verify(plain_password, stored_password)

# 工厂模式：用户创建工厂 Factory pattern: users create factories
class UserFactory:
    @staticmethod
    def create(request: RegisterRequest) -> User:
        return User(
            username=request.username,
            account=request.account,
            password=request.password,
            phone_number=request.phone_number,
            social_preference=request.social_preference,
            role=UserRole.NORMAL
        )

# 单例模式：Token 管理器 Singleton Pattern: Token Manager
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class TokenManager(metaclass=SingletonMeta):
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    def create_token(self, data: dict) -> str:
        expire = datetime.utcnow() + self.access_expire
        to_encode = {**data, "exp": expire}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)