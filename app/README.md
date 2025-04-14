# IIT 项目

## 项目结构

```
.
├── api/            # API 路由层
├── core/           # 核心配置
├── models/         # 数据库模型
├── schemas/        # 数据验证模式
├── services/       # 业务逻辑层
├── main.py         # 应用入口
└── requirements.txt # 项目依赖
```

## 主要功能

- 用户认证
- 商家管理
- 店铺管理

## 开发环境设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行服务器：
```bash
uvicorn main:app --reload
```

## API 文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc 