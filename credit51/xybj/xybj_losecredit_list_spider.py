# -*- coding: utf-8 -*-
import json
import random
import threading
from threading import current_thread

import requests

from ippool1 import ProxyIp
from config_xybj import USER_AGENT_LIST, DEFAULT_PROXYIP
from pipelines_xybj import FilePipelines, UniqueCheckPoint


class XybjLosecreditSpider(object):
    url = 'http://www.creditbj.gov.cn/xyData/front/creditService/getPageList.shtml'

    def __init__(self, page_num=1):
        self.User_Agent = random.choice(USER_AGENT_LIST)

        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'http://www.creditbj.gov.cn/xyData/front/creditService/initial.shtml?typeId=4',
            'Host': 'www.creditbj.gov.cn',
            'User-Agent': self.User_Agent,
            'Authorization': 'null',
            'Cookie': 'JSESSIONID=47323B995BD6349981D7155A6016AD5C; Hm_lvt_9a007596a40989746ba04af5b2cc3d40=1536567602,1537350891; Hm_lpvt_9a007596a40989746ba04af5b2cc3d40=1538012149',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.data = {
            'pageNo': page_num,
            'keyword': '',
            'typeId': 116,
        }

        self.proxies = {
            'http': DEFAULT_PROXYIP,
        }

    def set_proxies(self, proxyip):
        self.proxies = {
            'http': proxyip,
        }

    def get_info(self):
        response = None
        for i in range(3):
            proxyip = ProxyIp().get_ip()
            self.set_proxies(proxyip)
            print self.proxies
            try:
                response = requests.get(url=self.url, params=self.data, headers=self.headers, proxies=self.proxies,
                                        timeout=10)
                break
            except Exception as e:
                print e
        print 'response1:',response
        if not response:
            try:
                self.set_proxies(DEFAULT_PROXYIP)
                response = requests.get(url=self.url, params=self.data, headers=self.headers,proxies=self.proxies,
                                        timeout=10)
            except:
                print 'request timeout!!'
        print 'response2:',response
        return response

    def parse_res(self, response):
        fileio = FilePipelines()
        unique_check = UniqueCheckPoint()
        res_json = response.json()
        res_dict = json.loads(res_json)
        infos = res_dict['hits']['hits']
        judge_count = 0
        for info in infos:
            oid = info['_source']['id']
            isexist = unique_check.oid_isexist(oid)
            if isexist:
                judge_count += 1
            else:
                unique_check.to_mysql(oid)
                fileio.process_item(info)
        unique_check.close()
        return judge_count


class XybjLoseCredit(object):
    max_thread_num=2

    def work(self, start_pagenum, step):
        page_num = start_pagenum
        while True:
            myuser = XybjLosecreditSpider(page_num)
            response = myuser.get_info()
            if response:
                if response.text == '""':
                    print '{}: get the last page {}!!crawled complete!!'.format(current_thread().name, page_num)
                    break
                judge_count = myuser.parse_res(response)
                if judge_count >= 10:
                    print '{}: update to {} complete!!'.format(current_thread().name, page_num)
                    break
                print '{}: page {} write into files success!!'.format(current_thread().name, page_num)

            else:
                print 'request time out!! get page:%d faild!!' % page_num
            page_num += step


    def run(self):
        threads = []
        for i in range(1,self.max_thread_num+1):
            thr = threading.Thread(target=self.work, args=(i, self.max_thread_num))
            thr.start()
            threads.append(thr)
        for thr in threads:
            thr.join()


if __name__ == '__main__':
    XybjLoseCredit().run()
