import os
import json
import openai

from utils.log_control import write_log, LogType
from utils.prompt import get_prompt, get_system_prompt
from models.job import Job, Response
from utils.parser import Parser
from service.database_service import DatabaseService

class APIService:


    # 초기화
    def __init__(self):
        try: 
            self.api_key   = os.getenv("OPENAI_API_KEY")
            self.api_model = os.getenv("OPENAI_API_MODEL")
        except Exception as e:
            write_log(LogType.ERROR, "APIService.__init__", e)

    

    # API 상태 유효성 체크
    def is_valid_openai_api_status(self) -> bool: 
        try:
            if not self.api_key:
                raise ValueError("failed to load environment variable")

            self.client = openai.OpenAI(api_key=self.api_key)
            models_list = self.client.models.list()

            # env에 설정된 모델이 사용 가능한지 확인
            if not any(model.id == self.api_model for model in models_list.data):
                raise ValueError("the specified GPT model does not exist.")
            
            return True
        except Exception as e: 
            write_log(LogType.ERROR, "APIService.is_valid_api_status", e)
            return False



    # LLM 기반 에이전트 프로세스 실행
    def run_agent_process(self, database_service: DatabaseService) -> None:
        try: 
            parser = Parser()
            write_log(LogType.INFO, "run_agent_process", "entering run_agent_process")

            database_response = database_service.call_procedure("AGENT_JOB_CLASSIFIED_GET")
            job_list: Response = Response(body=[Job(*row) for row in database_response])
            MAX_ATTEMPTS = 5

            cnt = 0

            
            for job in job_list.body:
                job_model = None
                for attempt in range(MAX_ATTEMPTS):
                    openai_response = self.get_openai_response(get_prompt(job), get_system_prompt())
                    job_model = parser.validate_openai_response(openai_response) 
                    if job_model is not None:
                        break
                if job_model is None:
                    write_log(LogType.ERROR, "APIService.run_agent_process", f"job_no: {job.job_no} failed")
                    continue

                print(job_model)


                
                cnt = cnt + 1
                if cnt == 1: 
                    break


            database_service.close_pool()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.run_batch_process", e)




    # OpenAI API 호출
    def get_openai_response(self, prompt: str, system_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.api_model,
                response_format={"type": "json_object"},  
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}, 
                ],
                temperature=0.0 
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            write_log(LogType.ERROR, "APIService.get_openai_response", e)
            return None





    # 세션 종료
    def close_session(self) -> None:
        try:
            self.client.close()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.close_session", e)