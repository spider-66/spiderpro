# -*- coding: utf-8 -*-
import scrapy


class IptestspiderSpider(scrapy.Spider):
    name = 'iptestspider'
    allowed_domains = ['ip.cn']
    start_urls = ['https://ip.cn/']

    def parse(self, response):
        print response.text
