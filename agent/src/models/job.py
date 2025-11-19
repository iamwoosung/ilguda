from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass(kw_only=True)
class Job:
    job_no: int
    job_hash: str
    job_recruit_start_date: datetime
    job_recruit_end_date: datetime
    job_buspla_name: str
    job_cntct_no: str
    job_comp_addr: str
    job_emp_type: str
    job_enter_type: str
    job_job_nm: str
    job_offer_reg_date: datetime
    job_reg_date: datetime
    job_regagn_name: str
    job_req_career: str
    job_req_educ: str
    job_rno: int
    job_rnum: int
    job_salary: str
    job_salary_type: str

    # 작업 환경 필드
        
    job_env_both_hands: Optional[str] = None
    job_env_eyesight: Optional[str] = None
    job_env_handwork: Optional[str] = None
    job_env_lift_power: Optional[str] = None
    job_env_lstn_talk: Optional[str] = None
    job_env_stnd_walk: Optional[str] = None
    
    job_is_classified: int
    job_created_subject: int
    job_created_at: datetime
    job_updated_at: datetime



@dataclass
class Response:
    body: List[Job]