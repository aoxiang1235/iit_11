from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.store_review import StoreReview
from models.store import Store
from schemas.store_review import StoreReviewCreate

class StoreReviewService:
    @staticmethod
    async def create_review(
        db: Session,
        user_account: str,
        review_data: StoreReviewCreate
    ) -> StoreReview:
        """
        创建门店评价
        
        Args:
            db: 数据库会话
            user_account: 评价者账户
            review_data: 评价数据
            
        Returns:
            StoreReview: 创建的评价
            
        Raises:
            HTTPException: 当门店不存在时抛出异常
        """
        # 检查门店是否存在
        store = db.query(Store).filter(Store.id == review_data.store_id).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="门店不存在"
            )
            
        # 创建评价
        review = StoreReview(
            store_id=review_data.store_id,
            user_account=user_account,
            rating=review_data.rating,
            review_text=review_data.review_text
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return review
        
    @staticmethod
    async def get_store_reviews(
        db: Session,
        store_id: int
    ) -> list[StoreReview]:
        """
        获取门店的所有评价
        
        Args:
            db: 数据库会话
            store_id: 门店ID
            
        Returns:
            list[StoreReview]: 评价列表
        """
        return db.query(StoreReview).filter(StoreReview.store_id == store_id).all()
        
    @staticmethod
    async def get_user_reviews(
        db: Session,
        user_account: str
    ) -> list[StoreReview]:
        """
        获取用户的所有评价
        
        Args:
            db: 数据库会话
            user_account: 用户账户
            
        Returns:
            list[StoreReview]: 评价列表
        """
        return db.query(StoreReview).filter(StoreReview.user_account == user_account).all() 