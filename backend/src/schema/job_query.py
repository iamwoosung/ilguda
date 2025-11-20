import strawberry

from service import database_service
from utils.log_control import write_log, LogType

@strawberry.type
class JobQuery():

    @strawberry.field
    def hello(self) -> str:
        write_log(LogType.INFO, database_service.db_instance.test(), "tet")
        return "Hello from GraphQLService!"
