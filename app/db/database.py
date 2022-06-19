from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils.config import get_database_url


#  创建一个带连接池的引擎
#  * db_server默认空闲8小时断开connection
#  * pool_recycle=10800表示，connection空闲10800秒，自动重新获取
#  * 如果使用poolclass=NullPool参数将禁用连接池，关闭会话后立即断开数据库连接！！！
engine = create_engine(get_database_url(), pool_recycle=10800)


SessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # 关闭会话
        db.close()


Base = declarative_base()