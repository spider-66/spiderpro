# -*- coding: utf-8 -*-
import time
import os
import pymysql
# list1=os.listdir('/Users/wulian/Documents/wlcode/spiderprojects/spiderpros/credit51/files/2018-09-14')
# print len(list1),len(set(list1))

class Mysql(object):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = ''
    db = 'credit51'
    charset = 'utf8mb4'

    def __init__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                                   charset=self.charset)
        self.cursor = self.con.cursor()

    def run(self):
        result=self.cursor.execute("INSERT INTO cid290 (cid) SELECT '49772003' FROM dual WHERE not exists (select * from cid290 where cid290.cid = '49772003');")
        print result
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()

mysql=Mysql()
mysql.run()
mysql.close()

# import requests
# headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Language': 'en',
#         'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
#     }
# res=requests.get(url='https://bbs.51credit.com/forum-290-5.html',headers=headers,proxies={'http':'180.118.241.84:808'})
# print res.cookies