# -*- coding: utf-8 -*-

# ===========================文件路径=============================
BASE_DIR = '/opt/bigdata/cache'
SAVE_DIR = 'ods_radarx_f_xybj_losecredit_list'
KEYLIST = ['oname', 'area_name','unperform_part', 'area_id', 'type', 'gist_cid', 'opk_id', '@version', 'id', 'originalupdatetime',
           'court_name', 'performed_part', 'filelastupdatetime', 'performance1', 'disreput_type_name', 'lastupdatetime',
           'case_code','buesinessentity','rule_sign', 'is_show', 'reg_date', 'validstate', 'collecttime','@timestamp',
           'gist_unit','trans_dm_tong_insertdate', 'etcode', 'duty', 'creationtime', 'publish_date', 'status',
           'field0','field1','field2','field3']

# oname, onm , 失信名称
# area_name , are_nam , 区域名称
# unperform_part ,upf_prt , unperform_part
# area_id , are_aid ,区域编号
# type, typ, type
# gist_cid, gst_cid,gist_cid
# opk_id, opk_oid , opk_id
# @version, vsn, @version
# id , oid , 编号
# originalupdatetime ,org_udt_tim ,  originalupdatetime
# court_name ,crt_nam, 法院名称
# performed_part , pfm_prt, performed_part
# filelastupdatetime ,fil_lst_udt_tim , 文件最新更新时间
# performance1 ,pfm_pf1 , performance1
# disreput_type_name ,dis_rpt_typ_nam ,disreput_type_name
# lastupdatetime, lst_udt_tim,最近更新时间
# case_code ,cas_cod , case_code
# buesinessentity, bns_ett,buesinessentity
# rule_sign, rul_sig,rule_sign
# is_show,isw,is_show
# reg_date,reg_dat,reg_date
# validstate,vld_stt,validstate
# collecttime,clt_tim,收录时间
# @timestamp，tim_stp,@timestamp
# gist_unit,gst_unt,gist_unit
# trans_dm_tong_insertdate, tas_dmt_ist_dat , trans_dm_tong_insertdate
# etcode , etc_cod , etcode
# duty, dty , 失信职责
# creationtime, crt_tim ,creationtime
# publish_date, pls_dat , publish_date
# status ,stt , status
# field0 ,fld_fd0 ,field0
# field1 ,fld_fd1 ,field1
# field2 ,fld_fd2 ,field2
# field3 ,fld_fd3 ,field3


# ===========================user-agent list=============================
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


# ===========================proxyip========================
DEFAULT_PROXYIP='http://118.178.227.171:80'
