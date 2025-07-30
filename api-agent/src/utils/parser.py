import json
from typing import Dict, Any, List
import os
import sys

from models.response import Response, Body, Items, Item, Header
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Parser:
    
    @staticmethod
    def parse_json(data: Dict[str, Any]) -> Response:
        
        try:
            if 'response' in data:
                data = data['response']
            
            header_data = data.get('header', {})
            header = Header(
                result_code=header_data.get('resultCode', ''),
                result_msg=header_data.get('resultMsg', '')
            )
            
            body_data = data.get('body', {})
            items_data = body_data.get('items', {})
            
            item_list = []
            if 'item' in items_data:
                items = items_data['item']
                if not isinstance(items, list):
                    items = [items]
                
                for item_data in items:
                    item = Item(
                        rno=str(item_data.get('rno', '')),
                        rnum=str(item_data.get('rnum', '')),
                        buspla_name=item_data.get('busplaName', ''),
                        cntct_no=item_data.get('cntctNo', ''),
                        comp_addr=item_data.get('compAddr', ''),
                        emp_type=item_data.get('empType', ''),
                        enter_type=item_data.get('enterType', ''),
                        job_nm=item_data.get('jobNm', ''),
                        offerreg_dt=str(item_data.get('offerregDt', '')),
                        reg_dt=str(item_data.get('regDt', '')),
                        regagn_name=item_data.get('regagnName', ''),
                        req_career=item_data.get('reqCareer', ''),
                        req_educ=item_data.get('reqEduc', ''),
                        salary=item_data.get('salary', ''),
                        salary_type=item_data.get('salaryType', ''),
                        term_date=item_data.get('termDate', ''),
                        env_both_hands=item_data.get('envBothHands'),
                        env_eyesight=item_data.get('envEyesight'),
                        env_handwork=item_data.get('envHandWork'),
                        env_lift_power=item_data.get('envLiftPower'),
                        env_lstn_talk=item_data.get('envLstnTalk'),
                        env_stnd_walk=item_data.get('envStndWalk')
                    )
                    item_list.append(item)
            
            items = Items(
                item=item_list,
                num_of_rows=items_data.get('numOfRows', 0),
                page_no=items_data.get('pageNo', 0),
                total_count=items_data.get('totalCount', 0)
            )
            
            body = Body(items=items)
            
            return Response(header=header, body=body)
            
        except Exception as e:
            raise Exception(f"🔴 Fail(Parsing): {str(e)}")
    
    