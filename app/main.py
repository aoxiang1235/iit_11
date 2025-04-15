import sys
import os

# 将当前目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, merchant, store
from core.database import engine
from models import user, store as store_model, merchant as merchant_model, product

# 创建数据库表
user.Base.metadata.create_all(bind=engine)  # 先创建 user 表
merchant_model.Base.metadata.create_all(bind=engine)  # 再创建 merchant 表
store_model.Base.metadata.create_all(bind=engine)  # 再创建 store 表
product.Base.metadata.create_all(bind=engine)  # 最后创建 product 表

app = FastAPI(
    title="IIT API",
    description="IIT项目API文档",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含认证路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(merchant.router, prefix="/api/merchant", tags=["merchant"])
app.include_router(store.router, prefix="/api/store", tags=["store"])

@app.get("/")
async def root():
    return {"message": "Welcome to IIT API"} 