from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth import get_current_user
from models.user import User
from schemas.user import UserResponse

router = APIRouter()

@router.get("/userManger/queryAllUsers", response_model=List[UserResponse])
async def queryAllUsers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查询所有用户信息（仅管理员可用）
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        List[UserResponse]: 用户列表
        
    Raises:
        HTTPException: 当用户不是管理员时抛出403错误
    """
    # 检查用户角色
    if current_user.role != "administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查询所有用户信息"
        )
    
    # 查询所有用户
    users = db.query(User).all()
    return users 