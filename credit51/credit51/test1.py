# -*- coding: utf-8 -*-
import requests
import os
from requests.utils import should_bypass_proxies,get_environ_proxies
import json
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': USER_AGENT,
    # 'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%85%A8%E5%9B%BD%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&rsv_pq=e4fdc26d00013c62&rsv_t=ea63jXkfUYZ6trxyqfAb0nYRtRdA5lqPnxfsC4wupwswqvp%2Bf0KwATnXAZ8&rqlang=cn&rsv_enter=1&rsv_sug3=3',
    #      'Referer':'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%85%A8%E5%9B%BD%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&rsv_pq=fbdb532100025995&rsv_t=460672JI9RLNKi4NNAOSEmAKSFanwgoSSwULAgSNLwBBw7kdpviZ%2FD9RIg4&rqlang=cn&rsv_enter=1&rsv_sug3=3'
}

# http_url='http://ip111.cn/'
# https_url='https://i.qq.com/'
# https_url='https://www.baidu.com/'
https_url='https://www.ip.cn/'
url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'

proxies = {
    # 'https': 'http://124.117.246.106:48642',
    # 'https': 'https://221.239.108.36:80',
    'https': 'https://221.239.108.36:80',
}


#
# for j in range(103299,103300):
#     get_data = {
#         'resource_id': 6899,
#         'query': '全国失信被执行人名单',
#         'pn': j,
#         'ie': 'utf-8',
#         'oe': 'utf-8',
#         'format': 'json',
#     }
#     res = requests.get(url=url, headers=headers, proxies=proxies,params=get_data)
#     filename=str(j)+'.txt'
#     with open(filename,'a') as fp :
#         list1=res.json()['data'][0]['result']
#         for i in list1:
#             content=i['iname']+'\t'+i['gistId']+'\t'+i['courtName']+'\t'+i['loc']+'\t'+i['publishDate']+'\n'
#             fp.write(content.encode('utf-8'))


list1=[1,2,3,4,5]
print list1.index(1)