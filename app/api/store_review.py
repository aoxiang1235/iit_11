from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth import get_current_user
from schemas.store_review import StoreReviewCreate, StoreReviewResponse
from services.store_review import StoreReviewService
from models.user import User

router = APIRouter(
    prefix="/store-reviews",
    tags=["store-reviews"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=StoreReviewResponse)
async def create_review(
    review_data: StoreReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建门店评价
    
    Args:
        review_data: 评价数据
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StoreReviewResponse: 创建的评价
    """
    return await StoreReviewService.create_review(db, current_user.account, review_data)

@router.get("/store/{store_id}", response_model=List[StoreReviewResponse])
async def get_store_reviews(
    store_id: int,
    db: Session = Depends(get_db)
):
    """
    获取门店的所有评价
    
    Args:
        store_id: 门店ID
        db: 数据库会话
        
    Returns:
        List[StoreReviewResponse]: 评价列表
    """
    return await StoreReviewService.get_store_reviews(db, store_id)

@router.get("/my-reviews", response_model=List[StoreReviewResponse])
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有评价
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        List[StoreReviewResponse]: 评价列表
    """
    return await StoreReviewService.get_user_reviews(db, current_user.account) 