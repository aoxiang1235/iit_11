from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.store import Store
from models.user import User
from schemas.store import StoreCreate, StoreUpdate

class StoreService:
    @staticmethod
    async def create_store(db: Session, owner_account: str, store_data: StoreCreate) -> Store:
        """
        创建门店信息
        
        Args:
            db: 数据库会话
            owner_account: 门店归属人账户标识
            store_data: 门店信息数据
            
        Returns:
            Store: 创建的门店信息
            
        Raises:
            HTTPException: 当用户不存在时抛出异常
        """
        # 检查用户是否存在
        user = db.query(User).filter(User.username == owner_account).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
            
        # 创建门店信息
        store = Store(
            owner_account=owner_account,
            **store_data.model_dump()
        )
        
        db.add(store)
        db.commit()
        db.refresh(store)
        
        return store
        
    @staticmethod
    async def get_store(db: Session, store_id: int) -> Store:
        """
        获取门店信息
        
        Args:
            db: 数据库会话
            store_id: 门店ID
            
        Returns:
            Store: 门店信息
            
        Raises:
            HTTPException: 当门店不存在时抛出异常
        """
        store = db.query(Store).filter(Store.id == store_id).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="门店不存在"
            )
        return store
        
    @staticmethod
    async def update_store(
        db: Session,
        store_id: int,
        store_data: StoreUpdate
    ) -> Store:
        """
        更新门店信息
        
        Args:
            db: 数据库会话
            store_id: 门店ID
            store_data: 更新的门店信息
            
        Returns:
            Store: 更新后的门店信息
            
        Raises:
            HTTPException: 当门店不存在时抛出异常
        """
        store = await StoreService.get_store(db, store_id)
        
        # 更新门店信息
        for field, value in store_data.model_dump(exclude_unset=True).items():
            setattr(store, field, value)
            
        db.commit()
        db.refresh(store)
        
        return store
        
    @staticmethod
    async def get_stores_by_owner(db: Session, owner_account: str) -> list[Store]:
        """
        获取用户的所有门店
        
        Args:
            db: 数据库会话
            owner_account: 门店归属人账户标识
            
        Returns:
            list[Store]: 门店列表
        """
        return db.query(Store).filter(Store.owner_account == owner_account).all() 