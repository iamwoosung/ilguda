import sys

from utils.log_control import write_log, LogType
from config.environment import set_environment
from service.api_service import APIService


def run_agent_task(api_service: APIService):
    try:
        api_status = api_service.is_valid_api_status()
        if not api_status:
            raise ValueError("invalid api service status")

        write_log(LogType.INFO, "run_agent_task", "entering run_process_task")
        api_service.run_batch_process()
    except Exception as e:
        write_log(LogType.ERROR, "run_agent_task", e)
    finally:
        api_service.close_session()


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("process mode not selected")
        
        is_env_set = set_environment(sys.argv[1])
        if not is_env_set:
            raise ValueError("failed to load environment")
        
        run_agent_task(api_service=APIService())

    except Exception as e: 
        write_log(LogType.ERROR, "__main__", e)