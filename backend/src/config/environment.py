import os

from dotenv import load_dotenv
from utils.log_control import write_log, LogType

# 환경변수 설정
def set_environment(mode: str) -> bool: 
    try: 
        current_dir  = os.path.dirname(__file__)
        project_dir  = os.path.abspath(os.path.join(current_dir, '../', '../'))
        env_filename = {
            "production" : ".env.production",
            "dev"        : ".env.development",
        }
        dotenv_path = os.path.join(project_dir, env_filename[mode])

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path=dotenv_path)
        else:
            raise FileNotFoundError("load environment fail")
        
        write_log(LogType.INFO, "set_environment", "load environment success")
        return True
    except Exception as e: 
        write_log(LogType.ERROR, "set_environment", e)
        return False
    except FileNotFoundError as e: 
        write_log(LogType.ERROR, "set_environment", e)
        return False
    