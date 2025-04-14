from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.merchant import Merchant
from schemas.merchant import MerchantCreate, MerchantUpdate, MerchantApproval

class MerchantService:
    @staticmethod
    def create_merchant(db: Session, merchant: MerchantCreate, user_id: int) -> Merchant:
        """创建新商家"""
        db_merchant = Merchant(
            user_id=user_id,
            name=merchant.name,
            description=merchant.description,
            address=merchant.address,
            business_hours=merchant.business_hours,
            contact_phone=merchant.contact_phone,
            license_number=merchant.license_number,
            is_verified=False,
            is_open=True,
            status='pending'
        )
        db.add(db_merchant)
        db.commit()
        db.refresh(db_merchant)
        return db_merchant

    @staticmethod
    def get_merchant(db: Session, merchant_id: int) -> Optional[Merchant]:
        """获取商家信息"""
        return db.query(Merchant).filter(Merchant.id == merchant_id).first()

    @staticmethod
    def get_merchant_by_user_id(db: Session, user_id: int) -> Optional[Merchant]:
        """通过用户ID获取商家信息"""
        return db.query(Merchant).filter(Merchant.user_id == user_id).first()

    @staticmethod
    def get_merchants(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_verified: Optional[bool] = None
    ) -> List[Merchant]:
        """获取商家列表"""
        query = db.query(Merchant)
        if is_verified is not None:
            query = query.filter(Merchant.is_verified == is_verified)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_merchant(
        db: Session, 
        merchant_id: int, 
        merchant_update: MerchantUpdate
    ) -> Optional[Merchant]:
        """更新商家信息"""
        db_merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
        if not db_merchant:
            return None

        update_data = merchant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_merchant, field, value)

        db_merchant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_merchant)
        return db_merchant

    @staticmethod
    def approve_merchant(
        db: Session, 
        merchant_id: int, 
        approval: MerchantApproval
    ) -> Optional[Merchant]:
        """审核商家"""
        db_merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
        if not db_merchant:
            return None

        db_merchant.is_verified = approval.is_approved
        db_merchant.status = 'approved' if approval.is_approved else 'rejected'
        db_merchant.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_merchant)
        return db_merchant

    @staticmethod
    def delete_merchant(db: Session, merchant_id: int) -> bool:
        """删除商家"""
        db_merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
        if not db_merchant:
            return False

        db.delete(db_merchant)
        db.commit()
        return True 