import os
import openai

from utils.log_control import write_log, LogType
from service.database_service import DatabaseService

class APIService:


    # 초기화
    def __init__(self):
        try: 
            self.api_key   = os.getenv("OPENAI_API_KEY")
            self.api_model = os.getenv("OPENAI_API_MODEL")
        except Exception as e:
            write_log(LogType.ERROR, "APIService.__init__", e)

    


    def is_valid_openai_api_status(self) -> bool: 
        try:
            if not self.api_key:
                raise ValueError("failed to load environment variable")

            self.client = openai.OpenAI(api_key=self.api_key)
            models_list = self.client.models.list()

            if not any(model.id == self.api_model for model in models_list.data):
                raise ValueError("the specified GPT model does not exist.")
            
            return True
        except Exception as e: 
            write_log(LogType.ERROR, "APIService.is_valid_api_status", e)
            return False




    def run_agent_process(self, database_service: DatabaseService) -> None:
        try: 
            
            write_log(LogType.INFO, "run_agent_process", "entering run_agent_process")

            database_response = database_service.call_procedure("AGENT_JOB_CLASSIFIED_GET")
            print(database_response)

            database_service.close_pool()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.run_batch_process", e)





    def close_session(self) -> None:
        try:
            self.client.close()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.close_session", e)