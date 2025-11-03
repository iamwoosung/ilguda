from typing import Dict, Any

from models.job import Response, Job
from utils.log_control import write_log, LogType

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