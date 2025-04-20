from sqlalchemy import Column, Integer, String, Text, DateTime, func, CheckConstraint
from .user import Base

class StoreReview(Base):
    """
    门店评价模型类
    对应数据库中的 store_reviews 表
    包含门店评价信息
    """
    __tablename__ = "store_reviews"  # 数据库表名

    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键，唯一标识每条评价')
    
    # 关联的门店ID
    store_id = Column(Integer, nullable=False, comment='关联的门店ID')
    
    # 评价者的账户标识
    user_account = Column(String(100), nullable=False, comment='评价者的账户标识')
    
    # 评分，1-5分
    rating = Column(Integer, nullable=False, comment='评分，1-5分')
    
    # 评价内容，可为空
    review_text = Column(Text, comment='评价内容，可为空')
    
    # 评价时间，自动记录
    review_date = Column(DateTime, default=func.current_timestamp(), comment='评价时间，自动记录')
    
    # 添加评分范围检查约束
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    ) 