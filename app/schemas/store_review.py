from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreReviewBase(BaseModel):
    """评价基础模型"""
    rating: int = Field(..., ge=1, le=5, description="评分，1-5分")
    review_text: Optional[str] = Field(None, description="评价内容")

class StoreReviewCreate(BaseModel):
    """创建评价请求模型"""
    store_id: int = Field(..., description="门店ID")
    rating: int = Field(..., ge=1, le=5, description="评分，1-5分")
    review_text: Optional[str] = Field(None, description="评价内容")

class StoreReviewResponse(BaseModel):
    """评价响应模型"""
    id: int
    store_id: int
    user_account: str
    rating: int
    review_text: Optional[str]
    review_date: datetime

    class Config:
        from_attributes = True 