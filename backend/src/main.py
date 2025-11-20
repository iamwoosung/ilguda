import sys

from utils.log_control import write_log, LogType
from config.environment import set_environment

from service import database_service 
from service.database_service import DatabaseService
from service.graphql_service import GraphQLService

def run_server(graphql_service: GraphQLService, database_service: DatabaseService) -> None:
    try:
        # DB 상태 체크
        database_status = database_service.is_valid_database_status()
        if not database_status:
            raise Exception("database is not connected or invalid")
        
        # GraphQL 상태 체크
        graphql_status = graphql_service.is_valid_server_status()
        if not graphql_status:
            raise Exception("graphql server is not invalid")

        graphql_service.run_server()

    except Exception as e: 
        write_log(LogType.ERROR, "run_server", e)




if __name__ == "__main__":
    try:
        # 환경 변수 체크
        if len(sys.argv) < 2:
            raise ValueError("process mode not selected")
        is_env_set = set_environment(sys.argv[1])
        if not is_env_set:
            raise ValueError("failed to load environment")
        
        database_service.db_instance = DatabaseService()
        run_server(graphql_service=GraphQLService(), database_service=database_service.db_instance)

    except Exception as e: 
        write_log(LogType.ERROR, "__main__", e)