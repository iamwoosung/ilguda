import os
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from utils.log_control import write_log, LogType


class DatabaseService:
    
    # 초기화
    def __init__(self):
        self.db_host      : Optional[str] = os.getenv("DB_HOST")
        self.db_port      : int           = int(os.getenv("DB_PORT", 3306)) 
        self.db_user      : Optional[str] = os.getenv("DB_USER")
        self.db_password  : Optional[str] = os.getenv("DB_PASSWORD")
        self.db_name      : Optional[str] = os.getenv("DB_NAME")
        self.db_pool_size : int           = int(os.getenv("DB_POOL_SIZE", 10)) 
        
        self.engine: Optional[Engine] = None
        self.is_connected: bool = False
        self._database_url = \
            None if not all([self.db_host, self.db_user, self.db_password, self.db_name]) \
            else f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"


    # DB 상태 체크
    def is_valid_database_status(self) -> bool: 
        try:
            if not self._database_url: 
                raise ValueError("failed to load environment variables for DB URL")

            self.engine = create_engine(
                self._database_url,
                pool_size=self.db_pool_size,
                max_overflow=self.db_pool_size * 2,   # 풀 사이즈 초과 시 최대 생성 가능 연결 수
                pool_recycle=3600                     # 1시간마다 연결을 재활용하여 MySQL의 timeout 방지
            )
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))                
            self.is_connected = True
        except Exception as e:
            write_log(LogType.ERROR, "DatabaseService.is_valid_database_status", e)
            self.is_connected = False
            self.engine = None 
        return self.is_connected
    
    def test(self) -> bool:
        return self.is_connected
    
# 싱글톤
db_instance = None