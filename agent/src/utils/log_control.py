import os
import datetime
from enum import Enum

class LogType(Enum):
    INFO    = "INFO"
    WARNING = "WARNING"
    ERROR   = "ERROR"

# 로그 경로 찾기
def get_log_filepath() -> str:
    current_dir  = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, '../', '../', '../'))
    
    now = datetime.datetime.now() 
    year_month_str = now.strftime('%Y%m')
    day_str        = now.strftime('%d')
    
    log_dir = os.path.join(project_root, 'Log', year_month_str, day_str)
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, 'Agent.log')
    
    return log_file_path

# 로그 작성
def write_log(log_type: LogType, function_name: str, log_contents: str) -> None:
    try:
        log_filepath = get_log_filepath()
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_entry = f"[{timestamp_str}] [{log_type.name}] {function_name}: {log_contents}"
        print(log_entry)
        with open(log_filepath, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"[Error]: {e}")
