import sys

from utils.log_control import write_log, LogType
from config.environment import set_environment
from service.api_service import APIService
from service.database_service import DatabaseService


def run_agent_task(api_service: APIService, database_service: DatabaseService):
    try:
        # API 상태 체크
        api_status = api_service.is_valid_api_status()
        if not api_status:
            raise ValueError("invalid api service status")
        
        # DB 상태 체크
        database_status = database_service.is_valid_database_status()
        if not database_status:
            raise Exception("database is not connected or invalid")

        # 배치 프로세스 실행
        api_service.run_batch_process(database_service)
    except Exception as e:
        write_log(LogType.ERROR, "run_agent_task", e)
    finally:
        if api_service:
            api_service.close_session()
        if database_service:
            database_service.close_pool()


if __name__ == "__main__":
    try:
        # 환경 변수 체크
        if len(sys.argv) < 2:
            raise ValueError("process mode not selected")
        is_env_set = set_environment(sys.argv[1])
        if not is_env_set:
            raise ValueError("failed to load environment")
        
        run_agent_task(api_service=APIService(), database_service=DatabaseService())

    except Exception as e: 
        write_log(LogType.ERROR, "__main__", e)