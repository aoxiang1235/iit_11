from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class Merchant(Base):
    """
    商户模型类
    对应数据库中的 merchant 表
    包含商户的基本信息和经营信息
    """
    __tablename__ = "merchant"  # 数据库表名

    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, index=True)
    
    # 关联的用户ID，外键
    user_id = Column(Integer, ForeignKey("user.id"))
    
    # 商户名称，不能为空，最大长度100
    name = Column(String(100), nullable=False)
    
    # 商户描述，可以为空，最大长度500
    description = Column(Text)
    
    # 商户地址，不能为空，最大长度200
    address = Column(String(200))
    
    # 营业时间，可以为空，最大长度100
    business_hours = Column(String(100))
    
    # 联系电话，可以为空，最大长度20
    contact_phone = Column(String(20))
    
    # 营业执照号，可以为空，最大长度50
    license_number = Column(String(50))
    
    # 是否已验证，布尔类型，默认值为False
    is_verified = Column(Boolean, default=False)
    
    # 是否营业中，布尔类型，默认值为False
    is_open = Column(Boolean, default=True)
    
    # 创建时间，默认为当前时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 更新时间，默认为当前时间戳，在记录更新时自动更新
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    user = relationship("User")
    products = relationship("Product", back_populates="merchant")
    orders = relationship("Order", back_populates="merchant") 