import bisect
import json
import re
import datetime

log_file_path = '/var/log/dpkg.log'


def find(endless_haystack, needle):
    if endless_haystack[0] == needle:
        return 0

    i = 1
    hay = endless_haystack[i]
    while hay < needle:  # this is O(log n) where n is the index of the element
        i = 2 * i
        hay = endless_haystack[i]

    # from the loop before the element is between i and i // 2
    return bisect.bisect_left(endless_haystack, needle, i // 2, i)


async def read_logs_from_files(start_date: str = '2022-09-07', end_date: str = '2022-09-17',
                               per_page: int = 50, page_no: int = 1):
    # fetch latest logs 50---
    with open(log_file_path, "r") as f:
        logs = []
        regex = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"

        for item in f.readlines():
            match = re.search(regex, item)
            if match is not None:
                if datetime.datetime.strptime(start_date, '%Y-%m-%d') <= datetime.datetime.strptime(match.group(0),'%Y-%m-%d') <= datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                    logs.append(item)

        if page_no == 1:
            logs = logs[-per_page:]

        if page_no > 1:
            print(-(page_no * per_page), -(page_no - 1) * per_page, page_no)
            logs = logs[-(page_no * per_page): -(page_no - 1) * per_page]

        logs.reverse()
    return json.dumps({'logs': logs, 'page_no': page_no, 'per_page': per_page})
