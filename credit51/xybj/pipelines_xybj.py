# -*- coding: utf-8 -*-
import os

import pymysql

from get_save_path import get_save_path
from config_xybj import KEYLIST,SAVE_DIR


class FilePipelines(object):

    def process_item(self, item):
        key_list = KEYLIST
        oid = item['_source']['id']
        filename = str(oid) + '.txt'
        filepath = get_save_path(filename, SAVE_DIR)
        if not os.path.exists(filepath):
            fp = open(filepath, 'a')
            for key in key_list:
                value = item['_source'][key]
                if value:
                    fp.write(str(value) + '\t') if isinstance(value, int) else fp.write(
                        value.encode('utf-8').replace('\n', '').replace('\r', '').replace('\t','') + '\t')
                else:
                    fp.write('NULL' + '\t')
            fp.close()


class UniqueCheckPoint(object):
    host ='127.0.0.1'
    port =3306
    user ='root'
    password =''
    db = 'credit51'
    charset = 'utf8mb4'


    def __init__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                                   charset=self.charset)
        self.cursor = self.con.cursor()
        self.table = 'xybj_losecredit_checkpoint'
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