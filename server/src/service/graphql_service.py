import os
import uvicorn
import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from utils.log_control import write_log, LogType
from schema.schema import Query

class GraphQLService:
    
    def __init__(self):
        try:
            self.server_host   = os.getenv("SERVER_HOST")
            self.server_port   = int(os.getenv("SERVER_PORT"))
            self.server_reload = os.getenv("SERVER_RELOAD")
            self.server_title  = os.getenv("SERVER_TITLE")
        except Exception as e:
            write_log(LogType.ERROR, "GraphQLService.__init__", e)

        
    def is_valid_server_status(self) -> bool:
        try:
            return all([self.server_host, self.server_port, self.server_reload, self.server_title])
        except Exception as e: 
            write_log(LogType.ERROR, "GraphQLService.is_valid_server_status", e)
            return False
        

    def run_server(self) -> None:
        try: 
            # GraphQL 요청 Default는 카멜 표기법
            graphql_schema = strawberry.Schema(query=Query)
            graphql_router = GraphQLRouter(graphql_schema, path="/graphql", graphiql=True)

            app_instance = FastAPI(title=self.server_title)
            app_instance.include_router(graphql_router)
            
            uvicorn.run(
                app_instance,
                host   = self.server_host,
                port   = self.server_port,
                reload = False
            )
        except Exception as e: 
            write_log(LogType.ERROR, "GraphQLService.run_server", e)