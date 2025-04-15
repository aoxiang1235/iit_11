from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 数据库连接URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://rootMysql:190poLLLL@shao.mysql.database.azure.com:3306/p_iit"

# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 测试连接
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT username, password FROM users")
        for row in result:
            print(f"Username: {row[0]}, Password: {row[1]}")
    print("数据库连接成功！")
except Exception as e:
    print(f"数据库连接失败：{str(e)}") 