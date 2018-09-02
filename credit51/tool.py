#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyutil.common.procedure_helper import ProcedureBase, action


class Tool(ProcedureBase):
    default_db = "ods_radarx"

    def __init__(self, *args, **kwargs):
        super(Tool, self).__init__(*args, **kwargs)
        self.bucket_name = self.proplus.get_value_by_name("aws.s3.bucketName.radarx")

    @action
    def create_ods_radarx_f_credit51_comment(self):
        self.hive_execute("""
CREATE EXTERNAL TABLE `{self.db}.ods_radarx_f_credit51_comment`(
    pid STRING COMMENT '帖子id',
    ct1 STRING COMMENT '一级分类',
    ct2 STRING COMMENT '二级分类',
    tit STRING COMMENT '帖子主题',
    tit_url STRING COMMENT '帖子超链接',
    pst_atr STRING COMMENT '帖子作者',
    atr_url STRING COMMENT '作者链接',
    rls_tim STRING COMMENT '帖子发布时间',
    cid STRING COMMENT '评论id',
    cmt_atr STRING COMMENT '评论作者',
    cmt_atr_url STRING COMMENT '评论作者的id',
    atr_rls_tim STRING COMMENT '评论作者注册时间',
    flr STRING COMMENT '楼层',
    cmt STRING COMMENT '评论的内容'
) COMMENT '51信用卡帖子'
PARTITIONED BY (`day` string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\\t'
LINES TERMINATED BY '\\n'
STORED AS TEXTFILE
LOCATION 's3a://{self.bucket_name}/ods_radarx_f_credit51_comment'
;

grant all on table {self.db}.ods_radarx_f_credit51_comment to role {self.db}_all;
grant select on table {self.db}.ods_radarx_f_credit51_comment to role {self.db}_select;
""".format(self=self))

    @action
    def create_tables(self):
        self.create_ods_radarx_f_credit51_comment()
    
    @action
    def drop_ods_radarx_f_credit51_comment(self):
        self.hive_execute("drop table %s.%s" % (self.db, "ods_radarx_f_credit51_comment"))
        self.bash_execute("aws s3 rm --recursive s3://%s/%s" % (self.bucket_name, "ods_radarx_f_credit51_comment"))

    @action
    def drop_tables(self):
        self.drop_ods_radarx_f_credit51_comment()


if __name__ == "__main__":
    Tool().start()