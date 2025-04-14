from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.merchant import Merchant
from models.user import User
from schemas.merchant import MerchantCreate, MerchantUpdate, MerchantApproval

class MerchantService:
    @staticmethod
    async def create_merchant(db: Session, user_id: int, merchant_data: MerchantCreate) -> Merchant:
        """
        创建商家信息
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            merchant_data: 商家信息数据
            
        Returns:
            Merchant: 创建的商家信息
            
        Raises:
            HTTPException: 当用户不存在或已经是商家时抛出异常
        """
        # 检查用户是否存在
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
            
        # 检查用户是否已经是商家
        existing_merchant = db.query(Merchant).filter(Merchant.user_id == user_id).first()
        if existing_merchant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户已经是商家"
            )
            
        # 创建商家信息
        merchant = Merchant(
            user_id=user_id,
            status="pending",  # 初始状态为待审批
            **merchant_data.model_dump()
        )
        
        db.add(merchant)
        db.commit()
        db.refresh(merchant)
        
        return merchant
        
    @staticmethod
    async def get_merchant(db: Session, merchant_id: int) -> Merchant:
        """
        获取商家信息
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            
        Returns:
            Merchant: 商家信息
            
        Raises:
            HTTPException: 当商家不存在时抛出异常
        """
        merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="商家不存在"
            )
        return merchant
        
    @staticmethod
    async def update_merchant(
        db: Session,
        merchant_id: int,
        merchant_data: MerchantUpdate
    ) -> Merchant:
        """
        更新商家信息
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            merchant_data: 更新的商家信息
            
        Returns:
            Merchant: 更新后的商家信息
            
        Raises:
            HTTPException: 当商家不存在时抛出异常
        """
        merchant = await MerchantService.get_merchant(db, merchant_id)
        
        # 更新商家信息
        for field, value in merchant_data.model_dump(exclude_unset=True).items():
            setattr(merchant, field, value)
            
        db.commit()
        db.refresh(merchant)
        
        return merchant

    @staticmethod
    async def approve_merchant(
        db: Session,
        merchant_id: int,
        approval_data: MerchantApproval
    ) -> Merchant:
        """
        审批商家申请
        
        Args:
            db: 数据库会话
            merchant_id: 商家ID
            approval_data: 审批信息
            
        Returns:
            Merchant: 更新后的商家信息
            
        Raises:
            HTTPException: 当商家不存在或状态不正确时抛出异常
        """
        merchant = await MerchantService.get_merchant(db, merchant_id)
        
        # 检查商家状态是否为待审批
        if merchant.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该商家申请已经被处理"
            )
        
        # 更新商家状态
        merchant.status = "approved" if approval_data.approved else "rejected"
        if approval_data.reason:
            merchant.rejection_reason = approval_data.reason
            
        db.commit()
        db.refresh(merchant)
        
        return merchant 