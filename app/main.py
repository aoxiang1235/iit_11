import sys
import os

# 将当前目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, userManger, store, store_review, statistics

app = FastAPI(
    title="IIT API",
    description="IIT项目API文档",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3003", "http://localhost:3004", "http://localhost:3001", "http://localhost:3002", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含认证路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(store.router, prefix="/api/store", tags=["store"])
app.include_router(userManger.router, prefix="/api", tags=["userManger"])
app.include_router(store_review.router, prefix="/api", tags=["store-reviews"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])
@app.get("/")
async def root():
    return {"message": "Welcome to IIT API"} 