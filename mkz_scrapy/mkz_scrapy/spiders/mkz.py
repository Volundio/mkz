# -*- coding: utf-8 -*-
import scrapy
from mkz_scrapy.items import MkzScrapyItem
import re

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

class MkzSpidersSpider(scrapy.Spider):
    name = 'mkz_spiders'
    # allowed_domains = ['mkzhan.com']
    # start_urls = ['https://mkzhan.com/']

    def __init__(self, manhua_url=None, manhua_names=None, *args, **kwargs):
        self.server_link = 'https://www.mkzhan.com'
        # 将获得的数据赋值
        self.url = manhua_url
        self.manhua_name = manhua_names

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.zhangjie_parse)

    # 解析response，获取每个大章节链接地址和章节名
    def zhangjie_parse(self, response):
        # 获取章节链接地址
        urls = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/ul/li/a/@data-hreflink').extract()
        # 获取所有的章节名
        dir_names = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/ul/li/a/text()').extract()
        # 保存章节链接和章节名
        for index in range(len(urls)):
            dir_names[index]=validateTitle(dir_names[index].replace(' ','').replace("\n",''))
            link_url = self.server_link + urls[index]
            # print(dir_names[index])
            yield scrapy.Request(url=link_url,  callback=self.page_parse)

        # 解析每个章节中的图片链接
    def page_parse(self, response):
        pic_urls=response.xpath('/html/body/div[2]/div[2]/div/img/@data-src').extract()
        title=response.xpath('/html/body/div[2]/div[1]/div[2]/h1/a/text()').get()
        # 将获得的数据传入item
        item = MkzScrapyItem(pic_urls =pic_urls,title=title,big_title=self.manhua_name)
        yield item