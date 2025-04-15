from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.auth import  LoginResponse, RegisterRequest, UserRole
from schemas.user import User

from services.auth import get_password_hash, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

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
    hashed_password = get_password_hash(request.password)
    db_user = User(
        username=request.username,
        account=request.account,
        password=hashed_password,
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
    # 验证用户
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 检查用户是否被禁用
    if user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is disabled"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    # 返回登录响应
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        account=user.account,
        role=user.role,
        social_preference=user.social_preference
    ) 