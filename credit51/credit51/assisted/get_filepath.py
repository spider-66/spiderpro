# -*- coding: utf-8 -*-
import os
import datetime
from ..settings  import BASE_DIR,SQL_NAME

def get_filepath(conmentid):
    # current_dir_path = os.getcwd()

    # index = current_dir_path.rfind('/')
    # file_dir = current_dir_path[:index]

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')

    # 文件存放一级目录
    file_path1 = os.path.join('/Users/wulian/Documents/wlcode/spiderprojects/spiderpros/credit51', 'files')
    # file_path1 = BASE_DIR+'/'+SQL_NAME

    if not os.path.exists(file_path1):
        os.mkdir(file_path1)
    file_path2 = os.path.join(file_path1, nowTime)

    if not os.path.exists(file_path2):
        os.mkdir(file_path2)
    file_path3 = os.path.join(file_path2, conmentid)

    return file_path3

