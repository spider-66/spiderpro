# -*- coding: utf-8 -*-

import random
import logging
import threading

import requests
import pymysql
from lxml import etree



class ProxyIp(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    base_url = 'http://www.xicidaili.com/nn/{}'
    testhttps_url = 'https://www.baidu.com'
    # testhttp_url = 'http://ip111.cn/'

    mysql_host = '127.0.0.1'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = ''

    db_name = 'credit51'
    table_name = 'ippool'
    charset = 'utf8mb4'

    def __init__(self, logger=None):
        self.con = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
                                   password=self.mysql_password, db=self.db_name, charset=self.charset)
        self.cursor = self.con.cursor()
        try:
            self.cursor.execute('select * from {} limit 1'.format(self.table_name))
        except Exception as e:
            if e[-1] == u"Table '{}.{}' doesn't exist".format(self.db_name, self.table_name):
                self.cursor.execute(
                    'create table {}(id int primary key auto_increment,proxyip varchar(30) unique ,isvalid boolean default true ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table_name))
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)

    def check_url(self, key):
        proxies = {
            'https': key.lower()
        }
        # url = self.testhttps_url if key[:index] == 'https' else self.testhttp_url
        url = self.testhttps_url
        try:
            response1 = requests.get(url=url, headers=self.headers, proxies=proxies, timeout=10)
            return True if response1.status_code == 200 else False
        except Exception as e:
            print e
            return False

    def to_mysql(self, page_start, page_end):
        for i in range(page_start, page_end + 1):
            self.logger.debug('start crawl page{}'.format(i))
            response = requests.get(url=self.base_url.format(i), headers=self.headers)
            html_str = response.text
            etreeobj = etree.HTML(html_str)
            tr_list = etreeobj.xpath('//table/tr')
            for tr in tr_list[1:]:
                ip = tr.xpath('./td[2]/text()')[0]
                port = tr.xpath('./td[3]/text()')[0]
                style = tr.xpath('./td[6]/text()')[0].lower()
                key = style + '://' + ip + ':' + port
                if not self.ip_isexist(key):
                    if self.check_url(key):
                        try:
                            sql_insert = 'insert into {} (proxyip) value ("{}")'.format(self.table_name, key)
                            self.cursor.execute(sql_insert)
                            self.logger.debug('insert IP：%s success！' % key)
                            self.con.commit()
                        except Exception as e:
                            self.logger.error('Error:%s' % e)
                            # self.con.rollback()
            self.logger.debug('crawl and writed page{} complete！')

    def ip_isexist(self, key):
        sql_search = 'select proxyip from {} where proxyip="{}"'.format(self.table_name, key)
        return True if self.cursor.execute(sql_search) else False

    def update_proxyip(self):
        counter = 0
        LIMIT=100
        while True:
            tasks = []
            for i in range(8):
                self.con.ping(reconnect=True)
                sql_getall = 'select proxyip from {} limit {} offset {} '.format(self.table_name, LIMIT,LIMIT * counter)
                self.cursor.execute(sql_getall)
                results = self.cursor.fetchall()
                if not results:
                    break
                counter += 1
                thread = threading.Thread(target=self.update_worker, args=(results,))
                thread.start()
                tasks.append(thread)
            if not tasks:
                break
            for task in tasks:
                task.join()

    def update_worker(self, results):
        self.logger.info("update worker start")
        con = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user,
            password=self.mysql_password, db=self.db_name, charset=self.charset)
        cursor = con.cursor()
        for ip, in results:
            if not self.check_url(ip):
                sql_delete = 'update {} set isvalid=0 where proxyip="{}"'.format(self.table_name, ip)
                try:
                    con.ping(reconnect=True)
                    cursor.execute(sql_delete)
                    self.logger.debug('update invalid ip：%s' % ip)
                    con.commit()
                except Exception as e:
                    self.logger.debug('Error:%s' % e)
                    # self.con.ping(reconnect=True)
                    # self.con.rollback()
        cursor.close()
        con.close()

    def get_ip(self):
        sql_getall = 'select proxyip from {} where isvalid=1'.format(self.table_name)
        self.cursor.execute(sql_getall)
        results = self.cursor.fetchall()
        return random.choice(results)[0]

    def close(self):
        self.cursor.close()
        self.con.close()



