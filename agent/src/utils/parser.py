from typing import Dict, Any, Optional

from models.job import Job
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
    def get_test_classify_model() -> Optional[JobClassify]:
        validated_data: Dict[str, bool] = {
            'PhysicalDisability'    : False, 
            'BrainLesion'           : True, 
            'VisualImpairment'      : True, 
            'HearingImpairment'     : False, 
            'SpeechDisorder'        : False, 
            'FacialDeformity'       : True, 
            'KidneyDisorder'        : True, 
            'CardiacDisorder'       : True, 
            'LiverDisorder'         : True, 
            'RespiratoryDisorder'   : True, 
            'UrinaryDiversion'      : True, 
            'Epilepsy'              : True, 
            'IntellectualDisability': True, 
            'Autism'                : True, 
            'MentalIllness'         : True
        }
        return JobClassify(**validated_data)
 
    
    @staticmethod
    def get_procedure_params(job: Job, job_classify: JobClassify) -> tuple:
        try:
            if job is None or job_classify is None:
                raise ValueError("parameter is None")
            
            return (
                job.job_no, 
                job_classify.PhysicalDisability, 
                job_classify.BrainLesion, 
                job_classify.VisualImpairment, 
                job_classify.HearingImpairment, 
                job_classify.SpeechDisorder, 
                job_classify.FacialDeformity, 
                job_classify.KidneyDisorder, 
                job_classify.CardiacDisorder, 
                job_classify.LiverDisorder, 
                job_classify.RespiratoryDisorder, 
                job_classify.UrinaryDiversion, 
                job_classify.Epilepsy, 
                job_classify.IntellectualDisability, 
                job_classify.Autism, 
                job_classify.MentalIllness
            )
        except Exception as e:
            write_log(LogType.ERROR, "Parser.get_procedure_params", e) 
            return None