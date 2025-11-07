
from models.job import Job

def get_prompt(job: Job) -> str:
    
    # Response 스키마 정의
    json_schema_definition = {
        "PhysicalDisability": "Boolean",
        "BrainLesion": "Boolean",
        "VisualImpairment": "Boolean",
        "HearingImpairment": "Boolean",
        "SpeechDisorder": "Boolean",
        "FacialDeformity": "Boolean",
        "KidneyDisorder": "Boolean",
        "CardiacDisorder": "Boolean",
        "LiverDisorder": "Boolean",
        "RespiratoryDisorder": "Boolean",
        "UrinaryDiversion": "Boolean",
        "Epilepsy": "Boolean",
        "IntellectualDisability": "Boolean",
        "Autism": "Boolean",
        "MentalIllness": "Boolean"
    }
    job_details = f"""
        [채용 공고 상세 정보]
        1. 모집 직종: {job.job_nm}
        2. 사업장명 및 주소: {job.job_buspla_name} 

        [작업 환경 요구 사항 (없을 경우 'None' 출력)]
        - 양손 사용: {job.job_env_both_hands or 'None'}
        - 시력 요구: {job.job_env_eyesight or 'None'}
        - 손 작업: {job.job_env_handwork or 'None'}
        - 드는 힘: {job.job_env_lift_power or 'None'}
        - 듣고 말하기: {job.job_env_lstn_talk or 'None'}
        - 서거나 걷기: {job.job_env_stnd_walk or 'None'}
        """
    system_message = f"""
        당신은 고도로 전문화된 장애인 직무 적합성 분석가입니다.
        사용자가 제공하는 '채용 공고 상세 정보'와 '작업 환경 요구 사항'을 분석하여, 한국의 15가지 법적 장애 유형별로 해당 직무를 **성공적으로 수행할 수 있는지** 여부를 엄격하게 판단해야 합니다.

        판단 기준:
        1. **'작업 환경 요구 사항'**을 최우선으로 고려하십시오. (예: '듣고 말하기'가 필수라면 청각/언어 장애는 False)
        2. **'모집 직종'**의 일반적인 직무 특성(육체적/정신적 난이도, 반복성, 대인 접촉)을 고려하십시오.
        3. 응답은 오직 JSON 객체 형태여야 하며, 다음 스키마를 엄격히 따르십시오. 
        4. 응답값의 Key 순서 또한 다음 스키마의 Key 순서를 유지하십시오.

        {json_schema_definition}
        """
    user_message = f"""
        {job_details}

        위 정보를 분석하여 15가지 장애 유형별 수행 가능 여부를 True/False (Boolean) 값으로 JSON 형식에 맞게 출력하십시오. 추가적인 설명이나 서론/결론은 절대 포함하지 마십시오.
        """
    return system_message + user_message



def get_system_prompt() -> str:
    return "당신은 고도로 전문화된 장애인 직무 적합성 분석가입니다. 응답은 오직 JSON 객체 형태여야 합니다."