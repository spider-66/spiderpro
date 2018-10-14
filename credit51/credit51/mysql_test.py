# -*- coding: utf-8 -*-
import threading
from threading import current_thread,Lock
import pymysql
import random


class Mythread(threading.Thread):
    random.seed(2)
    random_numbers = random.sample(range(10000, 99999), k=1000)

    def __init__(self, *args, **kwargs):
        super(Mythread, self).__init__(*args, **kwargs)

    def run(self, ):
        while True:
            lock.acquire()
            if len(self.random_numbers) == 0:
                lock.release()
                break

            mysql = MysqlHelper()
            num = self.random_numbers.pop(-1)
            if not mysql.oid_isexist(num):
                mysql.to_mysql(num)
                print '{}:insert {} success!!'.format(current_thread().name, num)
                mysql.close()
            lock.release()
        print '{}:run over!!!'.format(current_thread().name)


class MysqlHelper(object):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password = ''
    db = 'test'
    charset = 'utf8mb4'

    def __init__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                                   charset=self.charset)
        self.cursor = self.con.cursor()
        self.table = 'concurrent_test'
        try:
            self.cursor.execute('select * from {} limit 1'.format(self.table))
        except Exception as e:
            if e[-1] == u"Table '{}.{}' doesn't exist".format(self.db, self.table):
                self.cursor.execute(
                    'create table {}(oid int primary key ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table))

    def to_mysql(self, oid):
        sql = 'insert into {} (oid) value({})'.format(self.table, oid)
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except Exception as e:
            print e

    def oid_isexist(self, oid):
        sql_select_lid = 'select oid from {self.table} where oid={oid}'.format(**locals())
        result = self.cursor.execute(sql_select_lid)
        return bool(result)

    def close(self):
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    list1 = []
    lock=Lock()
    for i in range(3):
        thr = Mythread()
        thr.start()
        list1.append(thr)
    for j in list1:
        j.join()
    print 'all over!!!'
