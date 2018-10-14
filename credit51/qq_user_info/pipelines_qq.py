# -*- coding: utf-8 -*-
import os

import pymysql

from config_qq import MYSQL_CONFIG,KEYLIST,SAVE_DIR
from qqutils import get_save_path



class MysqlPipelines(object):
    host = MYSQL_CONFIG['HOST']
    port = MYSQL_CONFIG['PORT']
    user = MYSQL_CONFIG['USER']
    password = MYSQL_CONFIG['PASSWORD']
    db = MYSQL_CONFIG['DB']
    charset = MYSQL_CONFIG['CHARSET']

    def __init__(self):
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db,
                                   charset=self.charset)
        self.cursor = self.con.cursor()
        self.table = 'qq_user_info'

        try:
            self.cursor.execute('select * from {} limit 1'.format(self.table))
        except Exception as e:
            if e[-1] == u"Table '{}.{}' doesn't exist".format(self.db, self.table):
                self.cursor.execute(
                    'create table {}(id int primary key auto_increment,qqn int unique ,crt_tim timestamp default current_timestamp ,udt_tim timestamp default current_timestamp on update current_timestamp ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table))

    def process_item(self, item):
        if self.qq_isexist(item['qqn']):
            sql = 'update {} set udt_tim=current_timestamp where qqn="{}"'.format(self.table, item['qqn'])
        else:
            sql = 'insert into {} (qqn) value("{}")'.format(self.table, item['qqn'])
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except:
            self.con.rollback()

    def qq_isexist(self, qqn):
        sql_select_qq = 'select qqn from {self.table} where qqn="{qqn}"'.format(**locals())
        result = self.cursor.execute(sql_select_qq)
        return bool(result)


class FilePipelines(object):

    def process_item(self, item):
        key_list = KEYLIST
        filename=str(item['qqn']) + '.txt'
        filepath = get_save_path.get_save_path(filename,SAVE_DIR)
        if not os.path.exists(filepath):
            fp = open(filepath, 'a')
            for key in key_list:
                value = item[key]
                if value and value != '-':
                    fp.write(str(value) + '\t') if isinstance(value, int) else fp.write(
                        value.encode('utf-8').replace('\n', '').replace('\r', '') + '\t')
                else:
                    fp.write('NULL' + '\t')
            fp.close()