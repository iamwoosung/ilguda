import os
import requests
from typing import Dict, Any

from utils.log_control import write_log, LogType
from utils.parser import Parser
from service.database_service import DatabaseService

class APIService:


    # 초기화
    def __init__(self):
        try: 
            self.api_base_url    = os.getenv("API_BASE_URL")
            self.api_key         = os.getenv("API_KEY")
            self.api_total_count = 0
            self.session         = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Connection': 'keep-alive'
            })
        except Exception as e:
            write_log(LogType.ERROR, "APIService.__init__", e)





    # API 정상 호출 가능한지 테스트용
    # 환경 변수 검증 및 total count 갱신
    def is_valid_api_status(self) -> bool: 
        try:
            if not self.api_base_url or not self.api_key:
                raise ValueError("failed to load environment variables(API_BASE_URL or API_KEY)")

            api_response = self.get_response(page_no=1, num_of_rows=1)
            if not api_response:
                raise ValueError("API response is empty or invalid")
            
            self.api_total_count=api_response['response']['body']['totalCount']
            return True
        except Exception as e: 
            write_log(LogType.ERROR, "APIService.is_valid_api_status", e)
            return False
        




    # API 호출 및 DB 저장 프로세스 실행
    def run_batch_process(self, database_service: DatabaseService):
        try: 
            parser = Parser()
            page_no, num_of_rows   = 1, 10
            count, api_total_count = 0, self.api_total_count

            write_log(LogType.INFO, "run_batch_process", "entering run_batch_process")


            # API 순차적으로 호출
            while count < api_total_count:
                api_response = self.get_response(page_no=page_no, num_of_rows=num_of_rows)
                job_list     = parser.parse_data(api_response)
                
                # 10개 단위로 API 호출, 응답 데이터 DB 저장
                for item in job_list.body:
                    params = parser.get_procedure_params(item)
                    database_response = database_service.call_procedure(proc_name="BATCH_JOB_SET", args=params)
                    write_log(LogType.INFO, "APIService.run_process_task", database_response[0])

                page_no += 1
                count   += len(job_list.body)
                # break

            database_service.close_pool()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.run_batch_process", e)





    # API 호출
    def get_response(self, page_no: int = 1, num_of_rows: int = 10, **kwargs) -> Dict[str, Any]:
        try:
            params = {
                'serviceKey': self.api_key,
                'pageNo'    : page_no,
                'numOfRows' : num_of_rows,
                **kwargs
            }
            response = self.session.get(
                url     = self.api_base_url, 
                params  = params, 
                timeout = 10
            )

            response.raise_for_status()
            if (response.status_code != 200):
                 raise ValueError(f"API request failed with status code: {response.status_code}")
            
            return response.json()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.get_data", e)
            return None




    # 세션 종료
    def close_session(self):
        try:
            self.session.close()
        except Exception as e:
            write_log(LogType.ERROR, "APIService.close_session", e)