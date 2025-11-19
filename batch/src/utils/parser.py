from typing import Dict, Any

from models.job import Response, Job
from utils.log_control import write_log, LogType
from utils.utils import hash_string, parse_to_datetime

class Parser:
    
    @staticmethod
    def parse_data(data: Dict[str, Any]) -> Response:
        try:
            data       = data['response'] if 'response' in data else data
            body_data  = data.get('body', {})
            items_data = body_data.get('items', {})
            raw_items  = items_data.get('item')
            item_list  = []
            
            if raw_items:
                items_to_process = raw_items if isinstance(raw_items, list) else [raw_items]
                
                for item_data in items_to_process:
                    item = Job(
                        term_date      =     item_data.get('termDate',   ''),
                        buspla_name    =     item_data.get('busplaName', ''),
                        cntct_no       =     item_data.get('cntctNo',    ''),
                        comp_addr      =     item_data.get('compAddr',   ''),
                        emp_type       =     item_data.get('empType',    ''),
                        enter_type     =     item_data.get('enterType',  ''),
                        job_nm         =     item_data.get('jobNm',      ''),
                        offerreg_dt    = str(item_data.get('offerregDt', '')),
                        reg_dt         = str(item_data.get('regDt',      '')),
                        regagn_name    =     item_data.get('regagnName', ''),
                        req_career     =     item_data.get('reqCareer',  ''),
                        req_educ       =     item_data.get('reqEduc',    ''),
                        rno            = str(item_data.get('rno',        '')),
                        rnum           = str(item_data.get('rnum',       '')),
                        salary         =     item_data.get('salary',     ''),
                        salary_type    =     item_data.get('salaryType', ''),
                        # 작업환경 관련 필드들
                        env_both_hands =     item_data.get('envBothHands'),
                        env_eyesight   =     item_data.get('envEyesight'),
                        env_handwork   =     item_data.get('envHandWork'),
                        env_lift_power =     item_data.get('envLiftPower'),
                        env_lstn_talk  =     item_data.get('envLstnTalk'),
                        env_stnd_walk  =     item_data.get('envStndWalk') 
                    )
                    item_list.append(item)
            return Response(body=item_list)
        except Exception as e:
            write_log(LogType.ERROR, "Parser.parse_data", e) 
            return Response(body=[])
        


    @staticmethod
    def get_procedure_params(data: Job) -> tuple:
        try:
            # 중복 방지를 위한 해시 생성
            # 삼성생명보험(주)+한국장애인고용공단 서울동부지사+사무 보조원(일반사업체)+2025-10-28~2025-11-10
            job_hash = hash_string(f"{data.buspla_name}+{data.regagn_name}+{data.job_nm}+{data.term_date}")
            term_parts = data.term_date.split('~')
            if not term_parts or len(term_parts) != 2:
                raise ValueError("invalid term_date format")
            
            job_recruit_start_date = parse_to_datetime(term_parts[0].replace('-', '')) if term_parts and term_parts[0] else None
            job_recruit_end_date   = parse_to_datetime(term_parts[1].replace('-', '')) if len(term_parts) > 1 and term_parts[1] else None
            job_offerreg_dt        = parse_to_datetime(data.offerreg_dt)
            job_reg_dt             = parse_to_datetime(data.reg_dt)

            if not all([job_hash, job_recruit_start_date, job_recruit_end_date, data.buspla_name, data.cntct_no,
                data.comp_addr, data.emp_type, data.enter_type, data.job_nm, job_offerreg_dt, 
                job_reg_dt, data.regagn_name, data.req_career, data.req_educ, data.rno,
                data.rnum, data.salary, data.salary_type]):
                raise ValueError("required fields are missing or invalid")

            return (
                job_hash, 
                job_recruit_start_date, 
                job_recruit_end_date,
                data.buspla_name,
                data.cntct_no,
                data.comp_addr,
                data.emp_type,
                data.enter_type,
                data.job_nm,
                job_offerreg_dt, 
                job_reg_dt, 
                data.regagn_name,
                data.req_career,
                data.req_educ,
                data.rno,
                data.rnum,
                data.salary,
                data.salary_type, 
                data.env_both_hands,
                data.env_eyesight,
                data.env_handwork,
                data.env_lift_power,
                data.env_lstn_talk,
                data.env_stnd_walk, 
                1 # 생성 주체 (1: 배치, 2: APP, 3: 관리자)
            )
        except Exception as e:
            write_log(LogType.ERROR, "Parser.get_procedure_params", e)
            return None