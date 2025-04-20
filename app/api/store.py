from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.auth import get_current_user
from schemas.store import StoreCreate, StoreUpdate, StoreResponse
from services.store import StoreService
from models.user import User

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    responses={404: {"description": "Not found"}},
)

@router.post("/apply", response_model=StoreResponse)
async def apply_store(
    store_data: StoreCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    申请门店入驻
    
    Args:
        store_data: 门店信息
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StoreResponse: 创建的门店信息
    """
    return await StoreService.create_store(db, current_user.account, store_data)

@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    """
    获取门店信息
    
    Args:
        store_id: 门店ID
        db: 数据库会话
        
    Returns:
        StoreResponse: 门店信息
    """
    return await StoreService.get_store(db, store_id)

@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: int,
    store_data: StoreUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新门店信息
    
    Args:
        store_id: 门店ID
        store_data: 更新的门店信息
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        StoreResponse: 更新后的门店信息
    """
    store = await StoreService.get_store(db, store_id)
    
    # 如果是审核操作（修改is_pass字段）
    if store_data.is_pass is not None:
        # 只有管理员可以审核
        if current_user.role != "administrator":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有管理员可以审核门店"
            )
    else:
        # 如果是修改其他信息，只有店主可以修改
        if store.owner_account != current_user.account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只有店主可以修改门店信息"
            )
    
    return await StoreService.update_store(db, store_id, store_data)

@router.get("/my/stores", response_model=List[StoreResponse])
async def get_my_stores(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有门店
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        List[StoreResponse]: 门店列表
    """
    return await StoreService.get_stores_by_owner(db, current_user.account)

@router.get("/all/stores", response_model=List[StoreResponse])
async def get_all_stores(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取所有门店（管理员专用）
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        List[StoreResponse]: 门店列表
    """
    # 只有管理员可以查看所有门店
    if current_user.role != "administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看所有门店"
        )
    return await StoreService.queryAllStores(db)

@router.get("/stats/types")
async def get_store_type_stats(
    store_id: int = None,
    db: Session = Depends(get_db)
):
    """
    获取商家类型统计
    
    Args:
        store_id: 可选的商家ID，如果提供则只统计该商家
        db: 数据库会话
        
    Returns:
        dict: 各类型商家的数量统计
            {
                "餐厅": 5,    # 键：商家类型，值：该类型的商家数量
                "KTV": 3,
                "咖啡店": 2,
                ...
            }
    """
    return await StoreService.get_store_type_stats(db, store_id)

@router.get("/stats/ratings")
async def get_rating_distribution(
    store_id: int = None,
    rating: int = None,
    db: Session = Depends(get_db)
):
    """
    获取评分分布统计
    
    Args:
        store_id: 可选的商家ID，如果提供则只统计该商家的评分
        rating: 可选的具体评分值（1-5），如果提供则只统计该评分的数量
        db: 数据库会话
        
    Returns:
        dict: 各评分等级的数量统计
            {
                "1": 10,   # 键：评分值（1-5星），值：该评分的数量
                "2": 20,
                "3": 30,
                "4": 40,
                "5": 50
            }
    """
    return await StoreService.get_rating_distribution(
        db, 
        store_id=store_id,
        rating=rating
    )