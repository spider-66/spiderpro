# -*- coding: utf-8 -*-
from selenium import webdriver
import csv
import time
import requests
import re

def get_detail_response(song_id):
    url = 'http://music.163.com/api/song/lyric?id={}&lv=-1&kv=-1&tv=-1'.format(song_id)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/'
    }
    response=requests.get(url,headers=headers)
    song_lrc=response.json()['lrc']['lyric'].encode('utf-8')
    return re.sub('\[\d{2}\:\d{2}\.\d{2}\]','',song_lrc).replace('\n',',')


def get_selenuim():
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get('https://music.163.com/#/song?id=554191055')
    driver.switch_to.frame('g_iframe')
    comments=driver.find_element_by_class_name('j-flag').text
    return comments

print get_detail_response('1305945750')