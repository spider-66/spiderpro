# -*- coding: utf-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB


class MySQL(object):
    host = 'localhost'
    user = 'root'
    port = 3306
    pasword = ''
    db = 'testDB'
    charset = 'utf8'

    pool = None
    limit_count = 3  # 最低预启动数据库连接数量

    def __init__(self):
        self.pool = PooledDB(pymysql, self.limit_count, host=self.host, user=self.user, passwd=self.pasword, db=self.db,
                             port=self.port, charset=self.charset, use_unicode=True)

    def select(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def insert(self, table, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            conn.rollback()
            return {'result': False, 'err': err}
        finally:
            cursor.close()
            conn.close()


