# -*- coding: utf-8 -*-
import time
import requests

def download_img(url,path,proxy):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    proxies={
        'https':'https://'+proxy,
    }
    response=requests.get(url=url,headers=headers,proxies=proxies)
    time.sleep(5)
    if response:
        with open(path,'wb') as fp:
            fp.write(response.content)
        return True
    else:
        return False
