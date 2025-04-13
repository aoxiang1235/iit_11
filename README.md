# IIT Project

这是一个基于FastAPI的后端项目。

## 环境要求

- Python 3.8+
- MySQL

## 安装

1. 克隆项目
```bash
git clone <repository-url>
cd iit_4
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制 `.env.example` 到 `.env` 并修改相应的配置

4. 运行项目
```bash
uvicorn app.main:app --reload
```

## API文档

启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
