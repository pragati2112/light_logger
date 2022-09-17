log_file_path = '/var/log/dpkg.log'


async def read_logs_from_files(start_date: str = '', end_date: str = '', per_page: int = 50):
    # fetch latest logs 50---
    with open(log_file_path, "r") as f:
        logs = f.readlines()[-per_page:]
    return logs
