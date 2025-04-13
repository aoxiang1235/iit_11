from fastapi import FastAPI
from .api import auth
from .core.database import engine
from .models import user

# 创建数据库表
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IIT Project API")

# 包含认证路由
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to IIT Project API"} 