# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Credit51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    ct1 = scrapy.Field()
    ct2 = scrapy.Field()
    tit = scrapy.Field()
    tit_url = scrapy.Field()
    pst_atr = scrapy.Field()
    atr_url = scrapy.Field()
    rls_tim = scrapy.Field()
    new_cmt_atr = scrapy.Field()
    new_cmt_tim = scrapy.Field()
    cid = scrapy.Field()
    cmt_atr = scrapy.Field()
    cmt_atr_url = scrapy.Field()
    atr_rls_tim = scrapy.Field()
    cmt = scrapy.Field()
    flr = scrapy.Field()
    total_pages_str=scrapy.Field()
    post_posi=scrapy.Field()
    com_posi=scrapy.Field()


    key_list = ['pid', 'ct1', 'ct2', 'tit', 'tit_url', 'pst_atr', 'atr_url', 'rls_tim', 'cid', 'cmt_atr', 'cmt_atr_url',
                'atr_rls_tim', 'flr', 'cmt']

    @classmethod
    def get_key_list(cls):
        dict_field = cls.__dict__['fields']
        return [key for key in dict_field]

class SinaTechItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    keyword = scrapy.Field()