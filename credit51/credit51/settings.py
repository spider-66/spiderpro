# -*- coding: utf-8 -*-

# Scrapy settings for credit51 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# ---------------------------------爬虫名称信息------------------------------

BOT_NAME = 'credit51'
SPIDER_MODULES = ['credit51.spiders']
NEWSPIDER_MODULE = 'credit51.spiders'

# ---------------------------------USER_AGENT配置------------------------------
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

# ---------------------------------Robots协议------------------------------
ROBOTSTXT_OBEY = True

# ---------------------------------下载延迟------------------------------
# DOWNLOAD_DELAY = 3

# ---------------------------------多线程并发------------------------------
# CONCURRENT_REQUESTS = 32                      # 并发请求数 默认16
# CONCURRENT_REQUESTS_PER_DOMAIN = 16            # 每个网域并发请求线程数
# CONCURRENT_REQUESTS_PER_IP = 16                # 每个ip并发请求数


# ---------------------------------cookie------------------------------
# COOKIES_ENABLED = False                        # cookie中间件的开启


# ---------------------------------请求头-----------------------------
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# ---------------------------------spider中间件-----------------------------
# SPIDER_MIDDLEWARES = {
#    'credit51.middlewares.Credit51SpiderMiddleware': 543,
# }

# ---------------------------------下载中间件-----------------------------
DOWNLOADER_MIDDLEWARES = {
    'credit51.middlewares.Credit51DownloaderMiddleware': 543,
    'credit51.middlewares.RandomProxyIpDownloaderMiddleware': 542,
    'credit51.middlewares.RandomUserAgentDownloaderMiddleware': 541,

}

# ---------------------------------item管道-----------------------------
ITEM_PIPELINES = {
    'credit51.pipelines.Credit51Pipeline': 400,
    'credit51.pipelines.Credit51MysqlPipeline': 302,
}


# ---------------------------------文件存放位置------------------------------
BASE_DIR = '/opt/bigdata/cache'
SQL_NAME = 'ods_radarx_f_credit51_comment'

# ---------------------------------redis配置-------------------------------------

REDIS_HOST = ''
REDIS_PORT = ''

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # request请求存放在redis中存放的key
SCHEDULER_PERSIST = True  # 关闭时是否保持请求记录和去重记录 true保持
SCHEDULER_FLUSH_ON_START = False  # 开始时是否清空之前的请求记录 false不清空

SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重保存的key

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"              # 调度器使用redis调度器
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  #去重类


# ---------------------------------日志文件-------------------------------------

# LOG_LEVEL = 'DEBUG'
