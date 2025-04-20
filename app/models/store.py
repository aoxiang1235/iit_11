from sqlalchemy import Column, Integer, String, DateTime, func
from .user import Base

class Store(Base):
    """
    门店模型类
    对应数据库中的 store 表
    包含门店的基本信息和经营信息
    """
    __tablename__ = "store"  # 数据库表名

    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 门店类型，不能为空，最大长度50
    store_type = Column(String(50), nullable=False)
    
    # 门店联系电话，可以为空，最大长度20
    store_phone = Column(String(20))
    
    # 门店详细地址，不能为空，最大长度255
    store_address = Column(String(255), nullable=False)
    
    # 门店营业时间，可以为空，最大长度100
    store_hours = Column(String(100))
    
    # 门店照片的存储路径或URL，可以为空，最大长度255
    store_photo = Column(String(255))
    
    # 门店归属人账户标识，不能为空，最大长度100
    owner_account = Column(String(100), nullable=False)
    
    # 创建时间，默认为当前时间戳
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # 审核状态，初始值0，通过1，驳回2
    is_pass = Column(Integer, default=0) 