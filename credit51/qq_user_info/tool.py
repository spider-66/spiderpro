#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import BUCKET
from spider_utils.procedure_helper import SpiderProcedureBase, action


class Tool(SpiderProcedureBase):
    default_db = "ods_radarx"

    def __init__(self, *args, **kwargs):
        super(Tool, self).__init__(*args, **kwargs)
        self.bucket_name = BUCKET

    @action
    def create_ods_radarx_f_qq_user_info(self):
        self.reset_proplus()
        self.hive_execute("""
CREATE EXTERNAL TABLE `{self.db}.ods_radarx_f_qq_user_info`(
    qq STRING COMMENT 'qq号码',
    psg_sig STRING COMMENT '个性签名',
    gdr STRING COMMENT '性别',
    btd STRING COMMENT '出生年月日',
    nik STRING COMMENT '昵称',
    mbl STRING COMMENT '手机',
    phn STRING COMMENT '电话',
    eml STRING COMMENT '邮箱',
    ara STRING COMMENT '所在地区',
    htn STRING COMMENT '故乡',
    cpn STRING COMMENT '个人说明',
    fac STRING COMMENT 'face',
    gdr_gid STRING COMMENT 'gender_id',
    alw STRING COMMENT 'allow',
    efg STRING COMMENT 'extflag',
    clg STRING COMMENT '大学',
    shx STRING COMMENT '生肖',
    sfg STRING COMMENT 's_flag',
    opn STRING COMMENT 'occupation',
    reg_typ STRING COMMENT 'reg_typ',
    hct STRING COMMENT 'h_city',
    cty_cid STRING COMMENT '城市编号',
    zne_zid STRING COMMENT '区域编号',
    pvc_pid STRING COMMENT '省份编号',
    cny_cid STRING COMMENT '国家编号',
    ctl STRING COMMENT '星座',
    bld STRING COMMENT '血型',
    png_url STRING COMMENT '头像url',
    sta STRING COMMENT 'stat',
    hpg STRING COMMENT '个人主页',
    flg STRING COMMENT 'flag'
) COMMENT 'qq用户信息'
PARTITIONED BY (`day` string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\\t'
LINES TERMINATED BY '\\n'
STORED AS TEXTFILE
LOCATION 's3a://{self.bucket_name}/ods_radarx_f_qq_user_info'
;

grant all on table {self.db}.ods_radarx_f_qq_user_info to role {self.db}_all;
grant select on table {self.db}.ods_radarx_f_qq_user_info to role {self.db}_select;
""".format(self=self))

    @action
    def create_tables(self):
        self.create_ods_radarx_f_qq_user_info()
    
    @action
    def drop_ods_radarx_f_qq_user_info(self):
        self.reset_proplus()
        self.hive_execute("drop table %s.%s" % (self.db, "ods_radarx_f_qq_user_info"))
        self.bash_execute("aws s3 rm --recursive s3://%s/%s" % (self.bucket_name, "ods_radarx_f_qq_user_info"))

    @action
    def drop_tables(self):
        self.drop_ods_radarx_f_qq_user_info()
    
    @action
    def create_mysql_qqpool(self):
        self.mysql_execute(u"""
CREATE TABLE `qqpool` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `qq` varchar(20) NOT NULL COMMENT 'QQ',
    `password` varchar(40) NOT NULL COMMENT '密码',
    `last_used_at` timestamp NULL COMMENT '最近使用时间',
    `isvalid` boolean default true COMMENT '可用',

    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `qq` (`qq`),
    KEY `idx_last_used_at` (`last_used_at`),
    KEY `idx_updated_at` (`updated_at`)
) ENGINE=InnoDB CHARSET=utf8mb4;
""")

    @action
    def create_mysql_qq_info_checkpoint(self):
        self.mysql_execute(u"""
CREATE TABLE `qq_info_checkpoint` (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `qq` varchar(20) NOT NULL COMMENT 'QQ',
    `proxyip` varchar(30) DEFAULT NOT NULL COMMENT '代理IP',
    `last_fetched_at` timestamp NULL COMMENT '最近抓取时间',

    `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `qq` (`qq`),
    KEY `idx_last_fetched_at` (`last_fetched_at`),
    KEY `idx_updated_at` (`updated_at`)
) ENGINE=InnoDB CHARSET=utf8mb4;
""")

    @action
    def create_mysql_tables(self):
        self.create_mysql_qqpool()
        # self.create_mysql_qq_info_checkpoint()


if __name__ == "__main__":
    Tool().start()