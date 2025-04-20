from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreBase(BaseModel):
    """门店基础信息模型"""
    store_type: str = Field(..., max_length=50, description="门店类型，例如餐厅、零售店")
    store_phone: Optional[str] = Field(None, max_length=20, description="门店联系电话")
    store_address: str = Field(..., max_length=255, description="门店详细地址")
    store_hours: Optional[str] = Field(None, max_length=100, description="门店营业时间")
    store_photo: Optional[str] = Field(None, max_length=255, description="门店照片的存储路径或URL")

class StoreCreate(StoreBase):
    """创建门店请求模型"""
    pass

class StoreUpdate(StoreBase):
    """更新门店信息请求模型"""
    store_type: Optional[str] = Field(None, max_length=50, description="门店类型，例如餐厅、零售店")
    store_address: Optional[str] = Field(None, max_length=255, description="门店详细地址")
    is_pass: Optional[int] = Field(None, description="审核状态：0-待审核，1-通过，2-驳回")

class StoreResponse(StoreBase):
    """门店信息响应模型"""
    id: int
    owner_account: str
    created_at: datetime
    is_pass: int

    class Config:
        from_attributes = True 