# -*- coding: utf-8 -*-
import time
from threading import current_thread

import numpy
import matplotlib.pyplot as plt
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from spider_utils.selenium_driver import chrome_driver
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

class SlidingVerifycodeHandler(object):
    # 滑动验证码
    # 此为腾讯空间滑动验证demo
    def __init__(self, username, password, url='https://i.qq.com/', proxy='https://221.239.108.36:80',
                 weidth_in_html=280, border=20):
        '''
        :param username: 用户名
        :param password: 密码
        :param url: 地址
        :param proxy: 代理
        :param weidth_in_html: 验证码img网页中显示的宽度
        :param border:  滑块起始位置与最左侧间距
        '''
        self.width_in_html = weidth_in_html
        self.border = border
        self.url = url
        self.proxy = proxy
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={}'.format(proxy.split('://')[-1]))
        options.add_argument('headless')
        options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
        self.browser = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.browser, 30)
        self.username = username
        self.password = password

    def __del__(self):
        self.browser.quit()

    def get_hold_button(self):
        """
        获取点击滑动按钮
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.ID, 'slideBlock')))
        return slider

    def get_img_url(self):
        element1 = WebDriverWait(self.browser, 50).until(lambda x: x.find_element_by_xpath('//iframe[@frameborder]'))
        self.browser.switch_to.frame(element1)
        print 'got verifycode frame:%s' % element1

        element2 = WebDriverWait(self.browser, 30).until(lambda x: x.find_element_by_id('slideBkg'))
        print 'got hold img:%s' % element2

        print "start to load verify code img"
        time.sleep(20)
        img_incomplete_url = element2.get_attribute('src')
        print 'got img_incomplete_url:%s' % img_incomplete_url
        img_complete_url = img_incomplete_url.replace('_1_', '_0_')
        return img_incomplete_url, img_complete_url

    def download_image(self, url, path):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        proxies = {
            'https': self.proxy,
            'http': self.proxy
        }
        response = requests.get(url=url, headers=headers, proxies=proxies)
        time.sleep(5)
        if response:
            with open(path, 'wb') as fp:
                fp.write(response.content)
            return True
        else:
            return False

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.ID, "login_frame")))
        self.browser.switch_to.frame('login_frame')
        self.browser.find_element_by_id('switcher_plogin').click()
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'u')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'p')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        self.browser.find_element_by_id('login_button').click()
        time.sleep(1)
        try:
            self.browser.find_element_by_id('login_button').click()
        except:
            pass

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        # 输入用户名密码
        self.open()
        # 获取验证码地址
        url1, url2 = self.get_img_url()
        # 下载验证码图片
        path1 = 'captcha1.png'
        path2 = 'captcha2.png'
        self.download_image(url1, path=path1)  # 缺口照片
        for i in range(7):
            time.sleep(5)
            result2 = self.download_image(url2, path=path2)
            if result2:
                print 'download complete img ok!!!'
                break
        else:
            print 'download faild'
        self.download_image(url2, path=path2)  # 完整照片
        # 获取缺口位置
        image1 = Image.open(path2)
        image2 = Image.open(path1)
        gap = self.get_gap(image1, image2)

        width = image1.size[0]
        width_in_html = self.width_in_html

        gap_in_html = round(gap * width_in_html / width)

        # 减去缺口位移
        gap_in_html -= self.border
        # 获取移动轨迹
        print gap_in_html
        track = self.get_track(gap_in_html)
        print track
        # 拖动滑块
        holder = self.get_hold_button()
        self.move_to_gap(holder, track)
        time.sleep(10)


# if __name__ == '__main__':
#     crack = SlidingVerifycodeHandler('123', 'qwe')
#     crack.crack()