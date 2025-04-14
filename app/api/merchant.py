from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth import get_current_user
from schemas.merchant import MerchantCreate, MerchantUpdate, MerchantResponse, MerchantApproval
from services.merchant import MerchantService
from models.user import User, UserRole

router = APIRouter(
    tags=["merchants"],
    responses={404: {"description": "Not found"}},
)

@router.post("/apply", response_model=MerchantResponse)
def apply_merchant(
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
    # 检查用户是否已经是商家
    existing_merchant = MerchantService.get_merchant_by_user_id(db, current_user.id)
    if existing_merchant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户已经是商家"
        )
    
    return MerchantService.create_merchant(db, merchant_data, current_user.id)

@router.get("/{merchant_id}", response_model=MerchantResponse)
def get_merchant(
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
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    return merchant

@router.put("/{merchant_id}", response_model=MerchantResponse)
def update_merchant(
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
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    
    if merchant.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改其他商家的信息"
        )
    
    updated_merchant = MerchantService.update_merchant(db, merchant_id, merchant_data)
    if not updated_merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    return updated_merchant

@router.post("/{merchant_id}/approve", response_model=MerchantResponse)
def approve_merchant(
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
    
    merchant = MerchantService.get_merchant(db, merchant_id)
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    
    approved_merchant = MerchantService.approve_merchant(db, merchant_id, approval_data)
    if not approved_merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="商家不存在"
        )
    return approved_merchant

@router.get("/", response_model=List[MerchantResponse])
def get_merchants(
    skip: int = 0,
    limit: int = 100,
    is_verified: bool = None,
    db: Session = Depends(get_db)
):
    """
    获取商家列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的最大记录数
        is_verified: 是否已认证
        db: 数据库会话
        
    Returns:
        List[MerchantResponse]: 商家列表
    """
    return MerchantService.get_merchants(db, skip, limit, is_verified) 