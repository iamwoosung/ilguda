from typing import Dict, Any, Optional

from models.job_classify import JobClassify 
from utils.log_control import write_log, LogType

class Parser:

    REQUIRED_KEYS = set(JobClassify.__dataclass_fields__.keys())

    @staticmethod
    def validate_openai_response(openai_response: Optional[Dict[str, Any]]) -> Optional[JobClassify]:
        try:
            if openai_response is None or not isinstance(openai_response, dict):
                raise ValueError("invalid OpenAI response format")
            
            response_keys = set(openai_response.keys())
            if response_keys != Parser.REQUIRED_KEYS:
                if Parser.REQUIRED_KEYS - response_keys:
                    raise ValueError("missing required keys in OpenAI response")
                
            validated_data: Dict[str, bool] = {}
            
            for key in Parser.REQUIRED_KEYS:
                value = openai_response.get(key)
                if not isinstance(value, bool):
                    raise ValueError(f"invalid type for key '{key}': expected bool")
                validated_data[key] = value

            return JobClassify(**validated_data)
        except Exception as e: 
                write_log(LogType.ERROR, "APIService.is_valid_api_status", e)
                return None
        
    @staticmethod
    def get_procedure_params(data: JobClassify) -> tuple:
        try:
            if data is None:
                raise ValueError("data is None")
            
            item_list = []
            for field in JobClassify.__dataclass_fields__.keys():
                item = getattr(data, field)
                if not isinstance(item, bool):
                    raise ValueError(f"invalid type for field '{field}': expected bool")
        except Exception as e:
            write_log(LogType.ERROR, "Parser.get_procedure_params", e) 
            return ()