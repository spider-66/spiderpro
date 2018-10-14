# -*- coding: utf-8 -*-
import pymysql
import threading
import random


class Db(object):
    def __init__(self, host=None, port=3306, username=None, pwd=None, dbname=None, charset='utf8mb4'):
        self.pool = {}
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.dbname = dbname
        self.charset = charset

    def get_instance(self, ):
        name = threading.current_thread().name
        if name not in self.pool:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.pwd,
                                   db=self.dbname, charset=self.charset)
            self.pool[name] = conn
        return self.pool[name]


class Mysql_helper(object):
    def __init__(self, worker,args=(),thread_nums=8):
        self.db = Db(host='127.0.0.1', username='root', pwd='', dbname='test', )
        self.lock = threading.Lock()
        self.thread_nums = thread_nums
        self.worker=worker
        self.args=args
        self.main()

    def main(self,):
        threads = []
        for i in range(self.thread_nums):
            t = threading.Thread(target=self.worker,args=self.args)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def sql_exexute(self,):
    db = self.db.get_instance()
    cursor = db.cursor()
    while True:
        with self.lock:
            if len(list1) == 0:
                break
            num=list1.pop(0)

            sql = 'INSERT INTO concurrent_test(oid) SELECT {} FROM DUAL WHERE NOT EXISTS(SELECT * FROM concurrent_test WHERE oid= {})'.format(num,num)
            try:
                cursor.execute(sql)
                db.commit()
                print(threading.current_thread().name, ': ', sql, ': success')
            except:
                db.rollback()
                print(threading.current_thread().name, ': ', sql, ':failed')
                raise


if __name__ == '__main__':

    list1 = [random.choice(range(10000, 99999)) for i in range(10000)]

    Mysql_helper(sql_exexute,args=(list1,))
