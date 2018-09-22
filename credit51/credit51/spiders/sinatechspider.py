# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jieba import analyse
from credit51.items import SinaTechItem

class SinatechspiderSpider(CrawlSpider):
    name = 'sinatechspider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://tech.sina.com.cn/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="tech-news"]/ul/li/a'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item =SinaTechItem()

        title=response.xpath('//h1[@id="artibodyTitle"]/text()').extract_first(default=u'暂无标题')
        date=response.xpath('//span[@id="pub_date"]/text()').extract_first(default=u'暂无时间')
        contents_list=response.xpath('//div[@id="artibody"]//text()').extract()
        content=''.join(contents_list)

        keyword=' '.join(analyse.extract_tags(content,topK=20))

        item['title']=title
        item['date']=date
        item['keyword']=keyword
        return item
