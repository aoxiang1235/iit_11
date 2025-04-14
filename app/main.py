import sys
import os

# 将当前目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, merchant, store
from core.database import engine
from models import user, store as store_model

# 创建数据库表
user.Base.metadata.create_all(bind=engine)
store_model.Base.metadata.create_all(bind=engine)

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
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(merchant.router)
app.include_router(store.router)

@app.get("/")
async def root():
    return {"message": "Welcome to IIT API"} 