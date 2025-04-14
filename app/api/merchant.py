from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth import get_current_user
from schemas.merchant import MerchantCreate, MerchantUpdate, MerchantResponse, MerchantApproval
from services.merchant import MerchantService
from models.user import User, UserRole

router = APIRouter(
    prefix="/merchants",
    tags=["merchants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/apply", response_model=MerchantResponse)
async def apply_merchant(
    merchant_data: MerchantCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    申请成为商家
    
    Args:
        merchant_data: 商家信息
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MerchantResponse: 创建的商家信息
    """
    return await MerchantService.create_merchant(db, current_user.id, merchant_data)

@router.get("/{merchant_id}", response_model=MerchantResponse)
async def get_merchant(
    merchant_id: int,
    db: Session = Depends(get_db)
):
    """
    获取商家信息
    
    Args:
        merchant_id: 商家ID
        db: 数据库会话
        
    Returns:
        MerchantResponse: 商家信息
    """
    return await MerchantService.get_merchant(db, merchant_id)

@router.put("/{merchant_id}", response_model=MerchantResponse)
async def update_merchant(
    merchant_id: int,
    merchant_data: MerchantUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新商家信息
    
    Args:
        merchant_id: 商家ID
        merchant_data: 更新的商家信息
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        MerchantResponse: 更新后的商家信息
    """
    # 检查是否是商家本人
    merchant = await MerchantService.get_merchant(db, merchant_id)
    if merchant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改其他商家的信息"
        )
    
    return await MerchantService.update_merchant(db, merchant_id, merchant_data)

@router.post("/{merchant_id}/approve", response_model=MerchantResponse)
async def approve_merchant(
    merchant_id: int,
    approval_data: MerchantApproval,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    审批商家申请
    
    Args:
        merchant_id: 商家ID
        approval_data: 审批信息
        current_user: 当前登录用户（必须是管理员）
        db: 数据库会话
        
    Returns:
        MerchantResponse: 更新后的商家信息
    """
    # 检查当前用户是否是管理员
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以审批商家申请"
        )
    
    return await MerchantService.approve_merchant(db, merchant_id, approval_data) 