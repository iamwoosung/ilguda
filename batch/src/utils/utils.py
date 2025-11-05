import hashlib
from datetime import datetime
from typing import Optional

from utils.log_control import write_log, LogType

def hash_string(input_string: str) -> str:
    try:
        encoded_string = input_string.encode('utf-8')
        sha256_hasher = hashlib.sha256()
        sha256_hasher.update(encoded_string)
        return sha256_hasher.hexdigest()
    except Exception as e:
        write_log(LogType.ERROR, "hash_string", e)
        return None



def parse_to_datetime(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str or len(date_str) < 8:
        return None
    try:
        return datetime.strptime(date_str[:8], '%Y%m%d') 
    except Exception as e:
        write_log(LogType.ERROR, "parse_to_datetime", e)
        return None