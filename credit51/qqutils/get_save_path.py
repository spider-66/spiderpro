# -*- coding: utf-8 -*-
import datetime
import os

from qq_user_info.config_qq import BASE_DIR


def get_save_path(qq, save_dir):

    nowdate = datetime.datetime.now().strftime('%Y-%m-%d')

    file_path1 = os.path.join('/Users/wulian/Documents/wlcode/spiderprojects/spiderpros/credit51/qq_user_info', 'files')
    # file_path1 = BASE_DIR+'/'+save_dir

    if not os.path.exists(file_path1):
        os.mkdir(file_path1)
    file_path2 = os.path.join(file_path1, nowdate)

    if not os.path.exists(file_path2):
        os.mkdir(file_path2)
    file_path3 = os.path.join(file_path2, qq)

    return file_path3
