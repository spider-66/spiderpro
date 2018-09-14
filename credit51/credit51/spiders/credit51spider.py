# -*- coding: utf-8 -*-
# encoding=utf-8

import logging
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from ..items import Credit51Item
from ..get_indexurl import get_allpart_indexurl
from ..pipelines import Credit51MysqlPipeline


class Credit51spiderSpider(scrapy.spiders.CrawlSpider):
    name = 'credit51spider'
    allowed_domains = ['bbs.51credit.com']
    start_url = 'http://bbs.51credit.com/'
    start_urls = get_allpart_indexurl(start_url)

    rules = (
        # 抽取每一页的link
        Rule(LinkExtractor(allow=r'forum-\d+-\d+\.html'),callback='parse_item', follow=True),
    )

    db_handler = Credit51MysqlPipeline()

    # 起始页的解析
    def parse_start_url(self, response):
        return self.parse_item(response)

    # 回调函数
    def parse_item(self, response):
        list1=[]
        list1.append(response.url)
        tbodys = response.xpath('//tbody[contains(@id,"thread")]')
        for tbody in tbodys:
            # 帖子主题
            tit = tbody.xpath('./tr/th/a[contains(@href,"thread")]/text()').extract_first(default=False)

            # 帖子作者
            pst_atr = tbody.xpath('./tr/td[@class="by"][1]/cite/a/text()').extract_first(default=False)

            # 作者链接
            author_base_url = tbody.xpath('./tr/td[@class="by"][1]/cite/a/@href').extract_first(default=False)
            atr_url = 'https://bbs.51credit.com/' + author_base_url

            # 发布时间
            rls_tim = tbody.xpath('./tr/td[@class="by"][1]/em/span/span/@title').extract_first(
                default=False) or tbody.xpath('./tr/td[@class="by"][1]/em/span/text()').extract_first(default=False)

            # 最新留言人
            new_cmt_atr = tbody.xpath('./tr/td[@class="by"][2]/cite/a/text()').extract_first(default=False)

            # 最新留言时间
            new_cmt_tim = tbody.xpath('./tr/td[@class="by"][2]/em/a/span/@title').extract_first(
                default=False) or tbody.xpath('./tr/td[@class="by"][2]/em/a/text()').extract_first(default=False)

            # 帖子具体分类
            # 大版块
            ct1 = tbody.xpath('//div[@class="z"]/a[3]/text()').extract_first(default=False)
            # 分区版块
            ct2 = tbody.xpath('//div[@class="z"]/a[4]/text()').extract_first(default=False)

            # 帖子id
            try:
                pid = tbody.xpath('./@id').extract_first(default=False).split('_')[-1]
            except:
                pid = False

            # 帖子总页数
            total_pages_str = tbody.xpath('./tr/td[@class="num"]/a/text()').extract_first(default=False)
            try:
                pages_num = int(total_pages_str) // 20 + 1
            except:
                pages_num = 0

            # 帖子大致位置
            str1 = response.url.split('-')[-1].split('.')[0]
            post_posi = u'part' + u'page' + str1

            # 帖子超链接
            title_base_url = tbody.xpath('./tr/th/a[contains(@href,"thread")]/@href').extract_first(default=False)
            # url_list1 = title_base_url.split('-')
            # if pages_num:
            #     for i in range(1, pages_num + 1):
            #         url_list1[-2] = str(i)
            #         title_url = '-'.join(url_list1)
            #         tit_url = 'https://bbs.51credit.com/' + title_url

            item = Credit51Item()
            item['pid'] = pid
            item['ct1'] = ct1
            item['ct2'] = ct2
            item['tit'] = tit
            item['pst_atr'] = pst_atr
            item['atr_url'] = atr_url
            item['rls_tim'] = rls_tim
            item['new_cmt_atr'] = new_cmt_atr
            item['new_cmt_tim'] = new_cmt_tim
            item['total_pages_str'] = total_pages_str
            item['post_posi'] = post_posi




            if self.db_handler.check_isupdate(pid, new_cmt_tim):
                yield scrapy.Request(url='https://bbs.51credit.com/' + title_base_url,callback=self.parse_comment_pageurl, meta={'item': item})

    def parse_comment_pageurl(self, response):

        item = response.meta['item']
        title_base_url = response.url
        total_pages_str = response.xpath('//div[@class="pgt"]//label/span/text()').extract_first(default=False)

        if total_pages_str:
            total_pages_list = re.findall('\d+', total_pages_str)
            total_pages = total_pages_list[0]
        else:
            total_pages = u'1'

        if total_pages.isdigit():
            for i in range(1, int(total_pages) + 1):
                if '-' in title_base_url:
                    url_list = title_base_url.split('-')
                    url_list[-2] = str(i)
                    tit_url = '-'.join(url_list)
                else:
                    post_id=title_base_url.split('=')[-1]
                    tit_url='https://bbs.51credit.com/thread-{}-{}-1.html'.format(post_id,i)

                item['tit_url'] = tit_url
                yield scrapy.Request(url=tit_url, callback=self.parse_card, meta={'item': item},dont_filter=True)

    def parse_card(self, response):
        item = response.meta['item']
        # 每一个评论的div标签
        divs = response.xpath('//div[@id="postlist"]/div[contains(@id,"post")]')
        for div in divs[:-1]:
            # 评论作者
            com_aut = div.xpath('.//div[@class="authi"]/a/text()').extract_first(default=False)

            # 评论作者的注册时间
            aut_rel_tim = div.xpath('.//dl[@class="pil cl"]/dd[5]/text()').extract_first(default=False)

            # 评论作者的url
            com_aut_url = 'https://bbs.51credit.com/' + div.xpath('.//div[@class="authi"]/a/@href').extract_first(
                default=False)

            # 评论的内容
            pattern = re.compile('^\(function\(\).*}\)\(\);', re.S)

            post_contents = div.xpath('.//td[contains(@id,"postmessage")]//text()').extract()
            post_content = ''.join(post_contents).strip()

            # 剔除抓取的js代码
            com = re.sub(pattern, '', post_content)

            # 评论的唯一id，用于判断更新
            cid = div.xpath('./@id').extract_first(default=False).split('_')[-1]

            # 楼层
            flr = div.xpath('.//div[@class="pi"]/strong/a/em/text()').extract_first(default=False)
            com_posi = u'{}/{}'.format(flr, int(item['total_pages_str']) + 1)

            item['cmt_atr'] = com_aut
            item['atr_rls_tim'] = aut_rel_tim
            item['cmt_atr_url'] = com_aut_url
            item['cmt'] = com
            item['cid'] = cid
            item['flr'] = flr
            item['com_posi'] = com_posi
            if not self.db_handler.cid_isexist(cid):
                yield item
