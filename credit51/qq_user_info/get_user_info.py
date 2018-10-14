# -*- coding: UTF-8 -*-

import requests
import random

import threading
from threading import current_thread

from qqutils.get_formdata import get_skey_byphone, get_ldw,get_skey
from qq_user_info.pipelines_qq import FilePipelines
from config_qq import QQ


class QQUserFinder(object):
    qq_finder_url = 'http://cgi.find.qq.com/qqfind/buddy/search_v3'
    skey = ''
    ldw = ''

    def __init__(self, qq, proxies, keyword=0):
        self.qq = qq
        self.headers = {
            'Host': 'cgi.find.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://find.qq.com/',
            'origin': 'http://find.qq.com',
            'Cookie': 'uin=o0%d; skey=%s;' % (self.qq, self.skey)
        }

        self.post_data = {
            'num': 20,
            'page': 0,
            'sessionid': 0,
            'keyword': keyword,
            'agerg': 0,
            'sex': 0,
            'firston': 1,
            'video': 0,
            'country': 1,
            'province': 61,
            'city': 1,
            'district': 0,
            'hcountry': 1,
            'hprovince': 0,
            'hcity': 0,
            'hdistrict': 0,
            'online': 1,
            'ldw': self.ldw
        }
        # self.proxies = {proxies.split('://')[0]: proxies.split('://')[1]}
        self.proxies = {'http':proxies}

    def set_keyword(self, keyword=0):
        self.post_data['keyword'] = keyword

    def set_skey_ldw(self):
        self.headers['Cookie'] = 'uin=o0%d; skey=%s;' % (self.qq, self.skey)
        self.post_data['ldw'] = self.ldw

    def get_response(self):
        response = None
        try:
            response = requests.post(url=self.qq_finder_url, data=self.post_data, headers=self.headers,
                                     proxies=self.proxies,timeout=20)
        except Exception as e:
            print e
        return response

    def parse(self):
        response = self.get_response()
        user_item = {}
        if response:
            response_json = response.json()
            print response_json

            info_dict = response_json['result']['buddy']['info_list'][0]

            # qq
            qq = info_dict['uin']
            # 个性签名
            personal_signature = info_dict['lnick']
            # 性别 男1 女2 未填225
            gender = info_dict['gender']
            # 出生年月日
            birthday = str(info_dict['birthday']['year']) + '-' + str(info_dict['birthday']['month']) + '-' + str(
                info_dict['birthday']['day'])
            # 昵称
            nick = info_dict['nick']
            # 手机
            mobile = info_dict['mobile']
            # 电话
            phone = info_dict['phone']
            # 邮箱
            email = info_dict['email']
            # 地区
            area = info_dict['country'] + info_dict['province'] + info_dict['city']
            # 故乡
            hometown = str(info_dict['h_country']) + str(info_dict['h_province']) + str(info_dict['h_zone'])
            # 说明
            caption = info_dict['personal']
            # face
            face=info_dict['face']
            # gender_id
            gender_id=info_dict['gender_id']
            # allow
            allow=info_dict['allow']
            # extflag
            extflag=info_dict['extflag']
            # 大学
            college=info_dict['college']
            # lnick
            lnick=info_dict['lnick']
            # cft_flag
            cft_flag=info_dict['cft_flag']
            # h_zone
            h_zone=info_dict['h_zone']
            # reg_type
            reg_type=info_dict['reg_type']
            # h_city
            h_city=info_dict['h_city']
            # city_id
            city_id=info_dict['city_id']
            # 生肖
            shengxiao=info_dict['shengxiao']
            # s_flag
            s_flag=info_dict['s_flag']
            # occupation
            occupation=info_dict['occupation']
            # zone_id
            zone_id=info_dict['zone_id']
            # province_id
            province_id=info_dict['province_id']
            # country_id
            country_id=info_dict['country_id']
            # 星座
            constel=info_dict['constel']
            # 血型
            blood=info_dict['blood']
            # 头像地址
            url=info_dict['url']
            # stat
            stat=info_dict['stat']
            # homepage,个人主页
            homepage=info_dict['homepage']
            # flag
            flag=info_dict['flag']


            user_item['qqn'] = qq
            user_item['psg_sig'] = personal_signature
            user_item['gdr'] = gender
            user_item['btd'] = birthday
            user_item['nik'] = nick
            user_item['mbl'] = mobile
            user_item['phn'] = phone
            user_item['eml'] = email
            user_item['ara'] = area
            user_item['htn'] = hometown
            user_item['cpn'] = caption
            user_item['fac'] = face
            user_item['gdr_gid'] = gender_id
            user_item['alw'] = allow
            user_item['efg'] = extflag
            user_item['clg'] = college
            user_item['lnk'] = lnick
            user_item['cft_flg'] = cft_flag
            user_item['hzn'] = h_zone
            user_item['reg_typ'] = reg_type
            user_item['hct'] = h_city
            user_item['cty_cid'] = city_id
            user_item['shx'] = shengxiao
            user_item['sfg'] = s_flag
            user_item['opn'] = occupation
            user_item['zne_zid'] = zone_id
            user_item['pvc_pid'] = province_id
            user_item['cny_cid'] = country_id
            user_item['ctl'] = constel
            user_item['bld'] = blood
            user_item['png_url'] = url
            user_item['sta'] = stat
            user_item['hpg'] = homepage
            user_item['flg'] = flag

        return user_item


class GetUserInfo(object):
    max_thread_num=1
    def work(self, keys):
        myUser = QQUserFinder(qq=QQ, proxies='http://118.178.227.171:80')
        proxy_format=myUser.proxies['http'].split('://')[-1]
        while True:
            key = random.choice(keys)
            try:
                # if myUser.get_response().json()['retcode'] != 0:
                    # myUser.skey = get_skey(QQ, PASSWORD, proxy_format)[0]
                myUser.skey = '@y0XlLw9KY'
                myUser.ldw = get_ldw(myUser.skey)
                myUser.set_skey_ldw()
                print '{} start to get {}'.format(current_thread().name, key)
                myUser.set_keyword(key)
                item = myUser.parse()
                global counter
                counter+=1
                print counter,item
                print '{} get {} over!!'.format(current_thread().name, key)
                # FilePipelines().process_item(item)
                # print '{} wirte {} over!!'.format(current_thread().name, key)
                # MysqlPipelines().process_item(item)
                # print '{} to mysql {} over!!'.format(current_thread().name, key)
            except Exception as e:
                # keys.append(key)
                print "get qq info failed: %s" % key

    def run(self,keys):
        threads = []
        for i in range(self.max_thread_num):
            thr = threading.Thread(target=self.work, args=(keys,))
            thr.start()
            threads.append(thr)
        for thr in threads:
            thr.join()


if __name__ == '__main__':
    keys=[122345454,323432586,33242156,675291234,324657290,23145276,546312389,324567132,123527584,34897654,99876743,76597652]
    counter = 0

    GetUserInfo().run(keys)
