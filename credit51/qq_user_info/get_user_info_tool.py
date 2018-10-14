# -*- coding: UTF-8 -*-

import os

from spider_utils.procedure_helper import SpiderProcedureBase, action
from procedure.qq_user_info.config_qq import SAVE_DIR

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class GetUserInfoTool(SpiderProcedureBase):
    default_db = "ods_radarx"

    def __init__(self, *args, **kwargs):
        super(GetUserInfoTool, self).__init__(*args, **kwargs)
        self.reset_proplus()
        self.max_thread_num = self.r.max_thread_num
        self.batch_num = self.r.batch_num
        self.crawl_remote_executor = self.r.crawl_remote_executor
        self.qq_sql = self.r.qq_sql
        self.min_qq = self.r.min_qq
        if self.qq_sql:
            self.qq_sql = " ".join(self.qq_sql)
        else:
            self.qq_sql = """
select qq
from dbank.loan_f_user_all_apply_qq
where qq != ''
group by qq
"""

    @property
    def work_script_path(self):
        return os.path.join(BASE_DIR, "get_user_info.py")

    @property
    def table_name(self):
        return SAVE_DIR

    def execute_remote_crawl_by_args(self, args):
        self.execute_remote_by_args(args, remote_executor=self.crawl_remote_executor)

    def collect_data(self):
        self.execute_remote_crawl_by_args(["/opt/bigdata/radarx/data_collect.py", "-a", "upload", "-file_max_lines", self.batch_num, "-table_name", self.table_name])
        self.hive_execute("MSCK REPAIR TABLE %s.%s" % (self.db, self.table_name))

    @action
    def run_single(self):
        self.collect_data()
        res = self.presto_execute_fetch("""
select qq_sql.qq
from (
%s
) as qq_sql
left join ods_radarx.ods_radarx_f_qq_user_info as user_info
on qq_sql.qq = user_info.qq
where qq_sql.qq is not null and qq_sql.qq != '' and user_info.qq is null
and qq_sql.qq > '%s'
group by qq_sql.qq
order by qq_sql.qq
limit %s
""" % (self.qq_sql, self.min_qq, self.batch_num))
        qqs = [qq for qq, in res]
        if qqs:
            self.min_qq = res[-1]
            self.execute_remote_crawl_by_args([self.work_script_path, "-qqs", ",".join(qqs), "-max_thread_num", self.max_thread_num])
            return True
        else:
            return False

    @action
    def run(self):
        count = 0
        while True:
            count += 1
            self.logger.info("running batch#%s" % count)
            res = self.run_single()
            self.logger.info("finished count: %s" % (count * self.batch_num,))
            if not res:
                break
        self.collect_data()
        

    def arg_parse(self, parser):
        super(GetUserInfoTool, self).arg_parse(parser)
        parser.add_argument('-batch_num', action='store', dest='batch_num', type=int, default=5000, help='Record count in a single batch')
        parser.add_argument('-max_thread_num', action='store', dest='max_thread_num', type=int, default=2, help='Max thread num')
        parser.add_argument('-crawl_remote_executor', action='store', dest='crawl_remote_executor', required=True, help='Crawl Remote Executor')
        parser.add_argument('-qq_sql', action='store', nargs='+', dest='qq_sql', default=None, help='SQL to get QQ')
        parser.add_argument('-min_qq', action='store', dest='min_qq', default='10000', help='Min QQ')


if __name__ == '__main__':
    GetUserInfoTool().start()
