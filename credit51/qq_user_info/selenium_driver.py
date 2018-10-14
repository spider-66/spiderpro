# -*- coding: utf-8 -*-
from contextlib import contextmanager

from selenium import webdriver


@contextmanager
def chrome_driver(proxy):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('--proxy-server={}'.format(proxy))
    # options.add_argument('user-agent="Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1"')
    options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
    driver = webdriver.Chrome(chrome_options=options)
    try:
        yield driver
    finally:
        driver.close()
        driver.quit()