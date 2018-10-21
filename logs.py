#log = """[21/Mar/2018 21:32:09] "GET https://sys.mail.ru/static/css/reset.css HTTPS/1.1" 200 1090"""
import re
from datetime import datetime
from urllib.parse import urlparse

def ignore_www(log):
    cut_www = re.sub(r'(://www.)', '', log)
    return(cut_www)

def ignore_urls(log, list_ignore_urls):
    if log in list_ignore_urls:
        return True
    else:
        return False

def start_at(request_date, start_date):
    if start_date > request_date:
        return True
    else:
        return False

def stop_at(request_date, stop_date):
    if stop_date < request_date:
        return True
    else:
        return False

def request_type(needed_type, request_type):
    if needed_type == request_type:
        return True
    else:
        return False

def slow_queries(list_top_five_slow):
    sum = 0
    for i in list_top_five_slow:
        sum += i
    return sum / 5

def ignore_files(url):
    url.path = re.search(r'//.+/.')
    if url.path:
        return True
    else:
        return False

def parse(
        ignore_files = False,
        ignore_urls = [],
        start_at = None,
        stop_at = None,
        request_type = None,
        ignore_www = False,
        slow_queries = False
):
    urls = {}
    top_five_list = []
    list_top_five_slow = []
    count = 0
    with open('log.log') as logs:
        for log in logs:
            format = '%d/%b/%Y %H:%M:%S'
            request_date = datetime.strptime(log[1:20], format)
            parse_line = re.search(r'\".*\"', log).group().strip('"')
            request_type_of_log, request, protocol = parse_line.split(' ')
            url = urlparse(request)
            parse_line = re.search(r' \d+ \d+', log).group().lstrip(' ')
            response_code, response_time = parse_line.split(' ')
            if ignore_files:
                if ignore_files(log):
                    continue
            if ignore_urls:
                if ignore_urls(log, ignore_urls):
                    continue
            if ignore_www:
                log = ignore_www(log)
            if start_at:
                if start_at(request_date, start_at):
                    continue
            if stop_at:
                if stop_at(request_date, stop_at):
                    continue
            if request_type:
                if request_type(request_type, request_type_of_log):
                    continue
            if slow_queries:
                if len(list_top_five_slow) < 5:
                    list_top_five_slow.append(response_time)
                elif len(list_top_five_slow) == 5:
                    list_top_five_slow.sort(reverse = True)
                    for i in list_top_five_slow:
                        if response_time < i:
                            list_top_five_slow.remove(i)
                            list_top_five_slow.append(response_time)

        if log not in urls.keys():
            urls[log] = 1
        else:
            urls[log] += 1

    if slow_queries:
            slow_queries_result = slow_queries(list_top_five_slow)
            print(slow_queries_result)

    for key in sorted(urls.keys()):
        top_five_list.append(key)
    print(top_five_list[:5])

