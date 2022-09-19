import bisect
import json
import re
import datetime

log_file_path = '/var/log/dpkg.log'
regex = r"([0-9]{4}-[0-9]{2}-[0-9]{2})"


def find_match(item: str = ''):
    match = re.search(regex, item)
    return datetime.datetime.strptime(match.group(0), '%Y-%m-%d')


def find(endless_haystack, needle):
    if find_match(endless_haystack[0]) == needle:
        return 0

    i = 1
    while i <= len(endless_haystack) and find_match(endless_haystack[i]) <= needle:
        # this is O(log n) where n is the index of the element
        i = 2 * i

    # from the loop before the element is between i and i // 2
    # return bisect.bisect_left(endless_haystack, needle, i // 2, i)
    return i//2, i


async def read_logs_from_files(start_date: str = '2022-09-07', end_date: str = '2022-09-17',
                               per_page: int = 50, page_no: int = 1):
    # fetch latest logs 50---
    with open(log_file_path, "r") as f:
        logs = []

        endless_hay = f.readlines()

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        start_idx, _ = find(endless_haystack=endless_hay, needle=start_date)
        _, end_idx = find(endless_haystack=endless_hay, needle=end_date)

        for item in endless_hay[start_idx: end_idx+1]:
            match = re.search(regex, item)
            if match is not None:
                matched_date = datetime.datetime.strptime(match.group(0), '%Y-%m-%d')
                if start_date <= matched_date <= end_date:
                    logs.append(item)

        if page_no == 1:
            logs = logs[-per_page:]

        if page_no > 1:
            print(-(page_no * per_page), -(page_no - 1) * per_page, page_no)
            logs = logs[-(page_no * per_page): -(page_no - 1) * per_page]

        logs.reverse()
    return json.dumps({'logs': logs, 'page_no': page_no, 'per_page': per_page})
