from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

# 创建基类，所有模型类都将继承这个基类
Base = declarative_base()

class UserRole(str, PyEnum):
    """用户角色枚举"""
    NORMAL = "normal"
    ADMINISTRATOR = "administrator"
    MERCHANT = "merchant"  # 修改为小写，与数据库保持一致

class User(Base):
    """
    用户模型类
    对应数据库中的 user 表
    包含用户的基本信息和权限控制
    """
    __tablename__ = "user"  # 数据库表名

    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 用户名，唯一，不能为空，最大长度50
    username = Column(String(50), unique=True, nullable=False)
    
    # 登录账号，唯一，不能为空，最大长度100
    account = Column(String(100), unique=True, nullable=False)
    
    # 密码，不能为空，最大长度255（存储加密后的密码）
    password = Column(String(255), nullable=False)
    
    # 电话号码，可以为空，最大长度20
    phone_number = Column(String(20))
    
    # 社交偏好，枚举类型，默认值为'None'
    social_preference = Column(String(8), default='None')
    
    # 用户角色，枚举类型，默认值为'normal'，不能为空
    role = Column(String(13), default=UserRole.NORMAL, nullable=False)
    
    # 是否禁用，布尔类型，默认值为False
    is_disabled = Column(Boolean, default=False)
    
    # 创建时间，默认为当前时间戳
    created_at = Column(DateTime, default=func.current_timestamp())
    
    # 更新时间，默认为当前时间戳，在记录更新时自动更新
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()) 