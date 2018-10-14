# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import requests
from lxml import etree
import pymysql
import json

url = 'http://www.creditbj.gov.cn/xyData/front/creditService/getPageList.shtml'
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'http://www.creditbj.gov.cn/xyData/front/creditService/initial.shtml?typeId=4',
    'Host': 'www.creditbj.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Authorization':'null',
    'Cookie':'JSESSIONID=47323B995BD6349981D7155A6016AD5C; Hm_lvt_9a007596a40989746ba04af5b2cc3d40=1536567602,1537350891; Hm_lpvt_9a007596a40989746ba04af5b2cc3d40=1538012149',
    'X-Requested-With':'XMLHttpRequest'
}

pagenum=1000
form_data = {
    'pageNo': pagenum,
    'keyword': '',
    'typeId': 116,
}

proxies={
    'http':'http://118.178.227.171:80'
}

response=requests.get(url=url,headers=headers,params=form_data,proxies=proxies,)
if response.text=='""':
    print 'the last page!!'
res_json=response.json()
print res_json
res_json=json.loads(res_json)
with open('%d.txt'%pagenum,'a') as fp:
    for hit in res_json['hits']['hits']:
        lid=hit['_source']['id']
        oname=hit['_source']['oname']
        case_code=hit['_source']['case_code']
        originalupdatetime=hit['_source']['originalupdatetime']
        fp.write(str(lid)+'\t'+oname.encode('utf-8')+'\t'+case_code.encode('utf-8')+'\t'+originalupdatetime.encode('utf-8')+'\n')

# def get_typeid():
#     base_url='http://www.creditbj.gov.cn/xyData/front/creditService/initial.shtml?typeId=4'
#     proxy='118.178.227.171:80'
#     options=webdriver.ChromeOptions()
#     options.add_argument('--proxy-server={}'.format(proxy))
#     options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
#     driver=webdriver.Chrome(chrome_options=options)
#     driver.get(base_url)
#     print driver.get_network_conditions()
#     driver.quit()
#
# get_typeid()
