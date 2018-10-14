# -*- coding: utf-8 -*-
import time
from threading import current_thread

import numpy
import matplotlib.pyplot as plt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from qq_user_info.selenium_driver import chrome_driver
from download_img import download_img

def get_tracks(distance):
    v = 0
    t = 0.2
    tracks = []

    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3

        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        tracks.append(round(s))
    return tracks


def get_distance(path1, path2):
    img1 = plt.imread(path1)
    img2 = plt.imread(path2)
    img3 = img2 - img1
    base = numpy.array([20, 20, 20])
    x, y, z = img3.shape
    for i in range(350, y):
        counter = 0
        for j in range(20, x):
            if (img3[j, i] > base).all():
                counter += 1
                if counter > 40:
                    return i, j


def get_skey(qq, password,proxy):
    print 'qq %s get skeying........., please wait!!' % qq
    with chrome_driver(proxy) as driver:
        driver.get('https://i.qq.com/')
        try:
            print 'try and start to get login_frame '
            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.ID, "login_frame"))
            )
        except Exception as e:
            raise Exception(e)

        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').send_keys(qq)
        time.sleep(1)
        driver.find_element_by_id('p').send_keys(password)
        time.sleep(1)
        driver.find_element_by_id('login_button').click()
        time.sleep(1)
        try:
            driver.find_element_by_id('login_button').click()
        except:
            pass
        print 'name and password write over'

        try:
            print 'try and start to get verifycode frame '
            element1=WebDriverWait(driver, 50).until(lambda x: x.find_element_by_xpath('//iframe[@frameborder]'))
            driver.switch_to.frame(element1)
            print 'got verifycode frame:%s'%element1

            element2 = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_id('slideBkg'))
            print 'got hold img:%s' % element2

            print "start to load verify code img"
            time.sleep(20)
            img_incomplete_url = element2.get_attribute('src')
            print 'got img_incomplete_url:%s'%img_incomplete_url

            img_complete_url = img_incomplete_url.replace('_1_', '_0_')


            filename1 = current_thread().name + 'incomplete.jpeg'
            filename2 = current_thread().name + 'complete.jpeg'

            print 'start to download incomplete img'
            result1=download_img(img_incomplete_url, filename1,proxy)
            print 'download incomplete img ok!!!' if result1 else 'download faild'

            print 'start to download complete img'
            for i in range(7):
                time.sleep(5)
                result2=download_img(img_complete_url, filename2,proxy)
                if result2:
                    print 'download complete img ok!!!'
                    break
            else:
                print 'download faild'

            screen_width = driver.get_window_size()['width']
            screen_height = driver.get_window_size()['height']

            img_width = screen_width * 0.35
            img_height = screen_height * 0.21

            x, _ = get_distance(filename1, filename2)
            print 'get the distance %d'%x
            offset = round((x * img_height) / img_width) - 16

            button = driver.find_element_by_id('slideBlock')
            ActionChains(driver).click_and_hold(button).perform()
            tracks = get_tracks(offset)
            print 'start to move the missing img '
            for i in tracks:
                ActionChains(driver).move_by_offset(xoffset=i, yoffset=0).perform()
            time.sleep(1)
            ActionChains(driver).release(button).perform()
            print 'verifycode verify complete!!'
            time.sleep(5)

        except Exception as e:
            print e

        print 'start to load qzone'
        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name('head-info'))
        driver.save_screenshot("test1.png")
        cookie_skey = driver.get_cookie('skey')
        cookie_p_skey = driver.get_cookie('p_skey')
        skey = cookie_skey['value']
        p_skey = cookie_p_skey['value']
        return skey, p_skey


def get_ldw(skey):
    base_num = 5381
    for i in range(len(skey)):
        base_num += (base_num << 5) + ord(skey[i])
    return base_num & 2147483647


def get_skey_byphone(qq, password,proxy):
    print 'qq %s get skeying........., please wait!!' % qq
    with chrome_driver(proxy) as driver:
        driver.get('https://i.qq.com/')
        time.sleep(1)
        driver.find_element_by_id('u').send_keys(qq)
        driver.find_element_by_id('p').send_keys(password)
        driver.find_element_by_id('go').click()
        time.sleep(1)
        try:
            driver.switch_to.frame('tcaptcha_iframe')
        except Exception as e:
            print e

        for i in range(15):
            time.sleep(1)
            try:
                screen_width=driver.get_window_size()['width']
                screen_height=driver.get_window_size()['height']

                img_width=screen_width*0.35
                img_height=screen_height*0.21

                img_incomplete_url = driver.find_element_by_id('bkBlock').get_attribute('src')
                img_complete_url = img_incomplete_url.replace('_1_', '_0_')

                filename1 = current_thread().name + 'incomplete.jpeg'
                filename2 = current_thread().name + 'complete.jpeg'

                download_img(img_incomplete_url, filename1,proxy)
                download_img(img_complete_url, filename2,proxy)
                time.sleep(0.5)

                x, _ = get_distance(filename1, filename2)
                offset = round((x * img_height) / img_width) - 15

                button = driver.find_element_by_id('slideBlock')
                ActionChains(driver).click_and_hold(button).perform()
                tracks = get_tracks(offset)
                for i in tracks:
                    ActionChains(driver).move_by_offset(xoffset=i, yoffset=0).perform()
                ActionChains(driver).release(button).perform()
                time.sleep(1)
                driver.save_screenshot('test.png')
            except Exception as e:
                print e

            cookie_skey = driver.get_cookie('skey')
            cookie_p_skey = driver.get_cookie('p_skey')
            if cookie_p_skey and cookie_skey:
                skey = cookie_skey['value']
                p_skey = cookie_p_skey['value']
                return skey, p_skey
        else:
            raise Exception("can not get cookie")

# print get_skey(3317781719,'sqcfv0487','221.239.108.36:80')