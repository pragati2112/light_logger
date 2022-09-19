import json
log_file_path = '/var/log/dpkg.log'


async def read_logs_from_files(start_date: str = '', end_date: str = '',
                               per_page: int = 50, page_no: int = 1):
    # fetch latest logs 50---
    with open(log_file_path, "r") as f:
        if page_no == 1:
            logs = f.readlines()[-per_page:]

        if page_no > 1:
            print(-(page_no * per_page), -(page_no-1)*per_page, page_no)
            logs = f.readlines()[-(page_no * per_page): -(page_no-1)*per_page]

        logs.reverse()
    return json.dumps({'logs': logs, 'page_no': page_no, 'per_page': per_page})
