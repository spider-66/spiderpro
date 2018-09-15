# -*- coding: utf-8 -*-

import requests, re



def get_allpart_indexurl(start_url):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': USER_AGENT
    }

    response = requests.get(url=start_url, headers=headers)
    # start_url_list = re.findall('forum-\d+-\d\.html', response.text)
    start_url_list = re.findall('forum-290-1\.html', response.text)
    start_url_list=['https://bbs.51credit.com/'+base_url for base_url in start_url_list]
    start_urls=list(set(start_url_list))

    return start_urls
