from http.client import responses

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
    # 检查是否是门店所有者
    store = await StoreService.get_store(db, store_id)
    if store.owner_account != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改其他门店的信息"
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
    return await StoreService.get_stores_by_owner(db, current_user.username)

@router.get("/all/stores", response_model=List[StoreResponse])
async def get_my_stores(
    db: Session = Depends(get_db)
):
    return await StoreService.queryAllStores(db)