from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .user import Base

class Merchant(Base):
    """
    商家模型类
    对应数据库中的 merchant 表
    包含商家的基本信息和经营信息
    """
    __tablename__ = "merchant"  # 数据库表名

    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 关联用户ID（外键）
    user_id = Column(Integer, ForeignKey('user.id'), unique=True, nullable=False)
    
    # 商家名称，不能为空，最大长度100
    name = Column(String(100), nullable=False)
    
    # 商家描述，可以为空，最大长度500
    description = Column(String(500))
    
    # 商家地址，不能为空，最大长度200
    address = Column(String(200), nullable=False)
    
    # 营业时间，可以为空，最大长度100
    business_hours = Column(String(100))
    
    # 联系电话，可以为空，最大长度20
    contact_phone = Column(String(20))
    
    # 营业执照号，可以为空，最大长度50
    license_number = Column(String(50))
    
    # 是否认证，布尔类型，默认值为False
    is_verified = Column(Boolean, default=False)
    
    # 是否营业中，布尔类型，默认值为True
    is_open = Column(Boolean, default=True)
    
    # 创建时间，默认为当前时间戳
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # 更新时间，默认为当前时间戳，在记录更新时自动更新
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 建立与用户表的关系
    user = relationship("User", backref="merchant") 