import datetime
import strawberry

from typing import Optional

@strawberry.input
class JobInput:
    job_buspla_name: str
    job_recruit_start_date: datetime
    job_recruit_end_date: datetime
    job_comp_addr: str
    job_emp_type: str
    job_enter_type: str
    
    job_req_career: Optional[str] = None
    job_req_educ: Optional[str] = None
    job_salary_type: Optional[str] = None 