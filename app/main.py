import sys
import os

# 将当前目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, store, user, userManger
from core.database import engine
from models import user as user_model, store as store_model, store_review

# 创建数据库表
user_model.Base.metadata.create_all(bind=engine)  # 先创建 user 表
store_model.Base.metadata.create_all(bind=engine)  # 再创建 store 表

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
app.include_router(store.router, prefix="/api/store", tags=["store"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(userManger.router, prefix="/api", tags=["userManger"])

@app.get("/")
async def root():
    return {"message": "Welcome to IIT API"} 