from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.store import Store
from models.user import User
from schemas.store import StoreCreate, StoreUpdate
from sqlalchemy import create_engine, text
import requests

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
        user = db.query(User).filter(User.account == owner_account).first()
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

    @staticmethod
    async def queryAllStores(db: Session) -> list[Store]:
        return db.query(Store).all()

    @staticmethod
    async def get_store_type_stats(
        db: Session, 
        store_id: int = None
    ) -> dict:
        """
        获取商家类型统计
        
        Args:
            db: 数据库会话
            store_id: 可选的商家ID
            
        Returns:
            dict: 各类型商家的数量统计
        """
        if store_id is not None:
            sql = text("SELECT store_type, COUNT(*) as count FROM store WHERE id = :store_id GROUP BY store_type")
            params = {"store_id": store_id}
        else:
            sql = text("SELECT store_type, COUNT(*) as count FROM store GROUP BY store_type")
            params = {}
            
        result = db.execute(sql, params).fetchall()
        return {store_type: count for store_type, count in result}

    @staticmethod
    async def get_rating_distribution(
        db: Session, 
        store_id: int = None,
        rating: int = None
    ) -> dict:
        """
        获取评分分布统计
        
        Args:
            db: 数据库会话
            store_id: 可选的商家ID
            rating: 指定具体评分
            
        Returns:
            dict: 各评分等级的数量统计
        """
        if store_id is not None and rating is not None:
            sql = text("""
                SELECT r.rating, COUNT(*) as count 
                FROM store_reviews r 
                JOIN store s ON r.store_id = s.id 
                WHERE s.id = :store_id AND r.rating = :rating
                GROUP BY r.rating 
                ORDER BY r.rating
            """)
            params = {"store_id": store_id, "rating": rating}
        elif store_id is not None:
            sql = text("""
                SELECT r.rating, COUNT(*) as count 
                FROM store_reviews r 
                JOIN store s ON r.store_id = s.id 
                WHERE s.id = :store_id
                GROUP BY r.rating 
                ORDER BY r.rating
            """)
            params = {"store_id": store_id}
        elif rating is not None:
            sql = text("""
                SELECT r.rating, COUNT(*) as count 
                FROM store_reviews r 
                JOIN store s ON r.store_id = s.id 
                WHERE r.rating = :rating
                GROUP BY r.rating 
                ORDER BY r.rating
            """)
            params = {"rating": rating}
        else:
            sql = text("""
                SELECT r.rating, COUNT(*) as count 
                FROM store_reviews r 
                JOIN store s ON r.store_id = s.id 
                GROUP BY r.rating 
                ORDER BY r.rating
            """)
            params = {}
            
        result = db.execute(sql, params).fetchall()
        distribution = {str(i): 0 for i in range(1, 6)}  # 初始化1-5星的计数为0
        for rating, count in result:
            distribution[str(rating)] = count
        return distribution

    @staticmethod
    async def get_state_stats():
        """
        获取各州商家数量统计
        
        Returns:
            list: 各州商家数量统计列表
        """
        try:
            # 构建Elasticsearch聚合查询
            query = {
                "size": 0,
                "aggs": {
                    "states": {
                        "terms": {
                            "field": "location.state",
                            "size": 50  # 获取前50个州的统计
                        }
                    }
                }
            }
            
            # 发送请求到Elasticsearch
            response = requests.get(
                "http://localhost:9200/chicago_yelp_bussinesses_reviewed/_search",
                headers={"Content-Type": "application/json"},
                json=query
            )
            
            if response.status_code != 200:
                print(f"从ES获取数据失败: {response.status_code}")
                return []
                
            data = response.json()
            if 'aggregations' not in data:
                print(f"从ES获取数据失败: {data}")
                return []
                
            # 转换数据格式
            buckets = data['aggregations']['states']['buckets']
            return [{"name": bucket["key"], "value": bucket["doc_count"]} 
                    for bucket in buckets]
                    
        except Exception as e:
            print(f"获取州统计数据时出错: {str(e)}")
            return []

