import strawberry

from typing import List, Optional
from datetime import datetime
from dataclasses import fields
from models.job import Job
from service import database_service
from utils.log_control import write_log, LogType

@strawberry.type
class JobQuery():

    @strawberry.field
    def jobs(
            self,
            jobBusplaName       : Optional[str] = None,  
            jobRecruitStartDate : Optional[datetime] = None,
            jobRecruitEndDate   : Optional[datetime] = None,
            jobCompAddr         : Optional[str]= None, 
            jobEmpType          : Optional[str]= None,
            jobEnterType        : Optional[str]= None, 
            jobReqCareer        : Optional[str]= None,
            jobReqEduc          : Optional[str]= None,
            jobSalaryType       : Optional[str]= None, 
            userID              : str = None
        ) -> List[Job]:
        try: 

            start_dt_str = jobRecruitStartDate.strftime('%Y-%m-%d %H:%M:%S') if jobRecruitStartDate else None
            end_dt_str = jobRecruitEndDate.strftime('%Y-%m-%d %H:%M:%S') if jobRecruitEndDate else None

            # 2. 튜플 인자 생성 (MySQL 프로시저의 파라미터 순서와 일치시켜야 함!)
            proc_args = (
                # 1) LIKE 검색:
                jobBusplaName, 
                jobCompAddr,
                # 2) DATETIME 검색:
                start_dt_str, 
                end_dt_str,
                # 3) EQUALS 검색:
                jobEmpType, 
                jobEnterType,
                jobReqCareer,
                jobReqEduc,
                jobSalaryType
            )
            database_response = database_service.db_instance.call_procedure("SERVER_JOB_LIST_GET", args=proc_args)
            job_list: List[Job] = [Job(**dict(zip([field.name for field in fields(Job)], row))) for row in database_response]
            return job_list
        except Exception as e: 
            write_log(LogType.ERROR, "run_server", e)
            return None
