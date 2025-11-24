from dataclasses import fields
import strawberry

from schema.job.input import JobInput
from models.job import Job
from server.src.service import database_service
from server.src.utils.log_control import write_log, LogType

@strawberry.type
class JobMutation:
    @strawberry.mutation
    def create_job(self, job_data: JobInput, userID: str) -> Job: 
        try:
            proc_args = (
                job_data.job_buspla_name,
                job_data.job_recruit_start_date.strftime('%Y-%m-%d %H:%M:%S'), 
                job_data.job_comp_addr,
                userID,
            )
            
            database_response = database_service.db_instance.call_procedure("SERVER_JOB_SET", args=proc_args)
            
            if database_response:
                row = database_response[0]
                job = Job(**dict(zip([field.name for field in fields(Job)], row)))
                return job
            
            raise Exception("Job creation failed in database.") 

        except Exception as e:
            write_log(LogType.ERROR, "create_job", e)
            return None