from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Job:
    term_date   : str                      # 모집기간
    buspla_name : str                      # 사업장명
    cntct_no    : str                      # 연락처
    comp_addr   : str                      # 사업장 주소
    emp_type    : str                      # 고용형태
    enter_type  : str                      # 입사형태
    job_nm      : str                      # 모집직종
    offerreg_dt : str                      # 구인신청일자
    reg_dt      : str                      # 등록일
    regagn_name : str                      # 담당기관
    req_career  : str                      # 요구경력
    req_educ    : str                      # 요구학력
    rno         : str                      # 순번
    rnum        : str                      # 순번
    salary      : str                      # 임금
    salary_type : str                      # 임금형태

    # 작업환경 관련 필드들
    env_both_hands : Optional[str] = None  # 작업환경_양손사용
    env_eyesight   : Optional[str] = None  # 작업환경_시력
    env_handwork   : Optional[str] = None  # 작업환경_손작업
    env_lift_power : Optional[str] = None  # 작업환경_드는힘
    env_lstn_talk  : Optional[str] = None  # 작업환경_듣고 말하기
    env_stnd_walk  : Optional[str] = None  # 작업환경_서거나 걷기





@dataclass
class Response:
    body: List[Job]