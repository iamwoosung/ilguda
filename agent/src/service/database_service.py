import os
from typing import Optional, Any, List, Tuple

from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector import Error

# 로깅 유틸리티가 있다고 가정
from utils.log_control import write_log, LogType


class DatabaseService:
    
    def __init__(self):
        self.db_host      : Optional[str] = os.getenv("DB_HOST")
        self.db_port      : int           = int(os.getenv("DB_PORT", 3306)) 
        self.db_user      : Optional[str] = os.getenv("DB_USER")
        self.db_password  : Optional[str] = os.getenv("DB_PASSWORD")
        self.db_name      : Optional[str] = os.getenv("DB_NAME")
        self.db_pool_size : int           = int(os.getenv("DB_POOL_SIZE", 10)) 

        self.connection_pool : Optional[MySQLConnectionPool] = None
        self.is_connected    : bool = False

    def is_valid_database_status(self) -> bool:
        try:
            if not all([self.db_host, self.db_user, self.db_password, self.db_name]):
                raise ValueError("Failed to load environment variables")            
            self.connection_pool = MySQLConnectionPool(
                pool_name="mysql_api_agent_pool",
                pool_size=self.db_pool_size,
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                autocommit=False
            )

            conn = self.connection_pool.get_connection()
            if conn.is_connected():
                self.is_connected = True
        except Error as e:
            write_log(LogType.ERROR, "DatabaseService.is_valid_database_status", e)
            self.is_connected = False
        finally:
            if conn:
                conn.close()
        return self.is_connected

    def call_procedure(self, proc_name: str, args: tuple = ()) -> List[Tuple[Any, ...]]:
        if not self.is_connected:
            raise RuntimeError("DB service is not connected or validated.")
            
        conn: Optional[PooledMySQLConnection] = None
        result: List[Tuple[Any, ...]] = []
        
        try:
            conn   = self.connection_pool.get_connection()
            cursor = conn.cursor()
            
            result_iterator = cursor.callproc(proc_name, args)
            
            # 2. 결과셋 처리 (첫 번째 결과셋만 가져오는 경우가 일반적)
            for single_result in result_iterator:
                # 결과셋이 튜플 리스트로 반환
                result = cursor.fetchall()
                break # 일반적으로 첫 번째 결과셋만 사용

            conn.commit()  # 변경 사항 커밋 (프로시저가 DML을 포함할 경우)
            
        except Error as e:
            error_msg = f"Procedure call failed ({proc_name}): {e}"
            write_log(LogType.ERROR, "DatabaseService.call_procedure", error_msg)
            if conn:
                conn.rollback() # 오류 발생 시 롤백
            raise # 예외를 호출자에게 다시 던져서 상위 로직에서 처리하게 함
            
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if conn:
                # 3. 연결을 풀에 반환 (가장 중요)
                conn.close() 

        return result

    def close_pool(self):
        """
        프로그램 종료 시 커넥션 풀의 모든 연결을 명시적으로 닫습니다.
        """
        if self.connection_pool:
            self.connection_pool.close()
            print("DB 커넥션 풀을 정상적으로 닫았습니다.")