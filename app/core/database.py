from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://rootMysql:190poLLLL@shao.mysql.database.azure.com:3306/p_iit"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # 连接池大小
    max_overflow=10,  # 超过 pool_size 后最多可以创建的连接数
    pool_timeout=30,  # 连接池中没有可用连接时的等待时间
    pool_recycle=1800,  # 连接在连接池中重复使用的时间间隔
    pool_pre_ping=True  # 每次连接前先测试连接是否有效
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 