from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Header:
    """API 응답 헤더 모델"""
    result_code: str
    result_msg: str


@dataclass
class Item:
    """데이터 아이템 모델"""
    rno: str
    rnum: str
    buspla_name: str
    cntct_no: str
    comp_addr: str
    emp_type: str
    enter_type: str
    job_nm: str
    offerreg_dt: str
    reg_dt: str
    regagn_name: str
    req_career: str
    req_educ: str
    salary: str
    salary_type: str
    term_date: str
    
    # 작업환경 관련 필드들
    env_both_hands: Optional[str] = None
    env_eyesight: Optional[str] = None
    env_handwork: Optional[str] = None
    env_lift_power: Optional[str] = None
    env_lstn_talk: Optional[str] = None
    env_stnd_walk: Optional[str] = None


@dataclass
class Items:
    """데이터 아이템들 모델"""
    item: List[Item]
    num_of_rows: int
    page_no: int
    total_count: int


@dataclass
class Body:
    """API 응답 바디 모델"""
    items: Items


@dataclass
class Response:
    """전체 API 응답 모델"""
    header: Header
    body: Body 