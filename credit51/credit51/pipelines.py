# -*- coding: utf-8 -*-
# encoding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time

import pymysql

from .assisted.get_filepath import get_filepath


class Credit51Pipeline(object):

    def process_item(self, item, spider):

        filepath = get_filepath(item['cid'] + '.txt')
        if not os.path.exists(filepath):
            fp = open(filepath, 'a')

            for key in item.key_list:
                if item[key]:
                    fp.write(item[key].encode('utf-8').replace('\n', '').replace('\r', '') + '\t')
                else:
                    fp.write('NULL' + '\t')

            fp.close()
        return item


class Credit51MysqlPipeline(object):
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
        self.table = 'tablepid290'
        self.table1 = 'credititem290'
        self.table_cid='cid290'
        try:
            self.cursor.execute('select * from {}'.format(self.table))
        except Exception as e:
            if e[-1] == u"Table '{}.{}' doesn't exist".format(self.db, self.table):
                self.cursor.execute(
                    'create table {}(id int primary key auto_increment,pid varchar(30) unique ,latest_time varchar(50),post_posi varchar(50) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table))
                self.cursor.execute(
                    'create table {}(id int primary key auto_increment,pid varchar(30),cid varchar(30),post_posi varchar(50),com_posi varchar (50)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table1))

        try:
            self.cursor.execute('select * from {} limit 2'.format(self.table_cid))
        except Exception as e:
            if e[-1] == u"Table '{}.{}' doesn't exist".format(self.db, self.table_cid):
                self.cursor.execute(
                    'create table {}(cid int unique ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4'.format(
                        self.table_cid))



    def process_item(self, item, spider):
        if self.pid_isexist(item['pid']):
            sql = 'update {} set latest_time="{}" where pid="{}"'.format(self.table, item['new_cmt_tim'], item['pid'])
        else:
            sql = 'insert into {} (pid, latest_time,post_posi) value("{}", "{}","{}")'.format(self.table, item['pid'],
                                                                                              item['new_cmt_tim'],
                                                                                      item['post_posi'])
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except:
            self.con.rollback()

        sql_insert = 'insert into {} (pid, cid,post_posi,com_posi) value("{}", "{}","{}","{}")'.format(self.table1,
                                                                                                       item['pid'],
                                                                                                       item['cid'],
                                                                                                       item[
                                                                                                           'post_posi'],
                                                                                                       item['com_posi'])

        self.cursor.execute(sql_insert)
        self.con.commit()

        sql_insert_cid = 'insert into {} (cid) value("{}")'.format(self.table_cid, int(item['cid']))
        try:
            self.cursor.execute(sql_insert_cid)
            self.con.commit()
        except:
            self.con.rollback()




        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.con.close()

    def pid_isexist(self, pid):
        sql_select_pid = 'select pid from {self.table} where pid="{pid}"'.format(**locals())
        result = self.cursor.execute(sql_select_pid)
        return bool(result)

    def check_isupdate(self, pid, new_com_tim):
        sql_select_pid = 'select pid from {self.table} where pid="{pid}" and latest_time < "{new_com_tim}"'.format(
            **locals())
        result = self.cursor.execute(sql_select_pid)
        return not bool(result)

    def cid_isexist(self, cid):
        sql_cid = 'INSERT INTO {self.table_cid} (cid) SELECT {cid} FROM dual WHERE not exists (select * from {self.table_cid} where {self.table_cid}.cid = {cid});'.format(**locals())
        result = self.cursor.execute(sql_cid)
        # 存在返回0，不存在返回1并插入
        return bool(result)