# from scrapy import cmdline
import sys
import requests
import prettytable as pt
import re
from bs4 import BeautifulSoup
import os
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mkz_scrapy.spiders.mkz import MkzSpidersSpider


import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def get_manhua_inf():
    Keyword = input('请输入漫画名。\n')
    root_url = 'https://www.mkzhan.com/search/?keyword='+Keyword
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
        "method": "GET",
        "schemed": "https",
        "authority": "www.mkzhan.com",
    }
    rs = requests.get(root_url, headers=headers)
    if rs.status_code == 403:
        print('403 服务器拒绝请求')
        return ''
    if rs.status_code == 404:
        print('404 not found')
        return ''
    soup = BeautifulSoup(rs.text, 'html.parser')
    list_content = soup.find_all("a", {"class": 'cover'})
    nameList=soup("img", {"class": 'lazy'})
    rs.close()
    # templist = etree.HTML(rs.text).xpath('/html/body/div[2]/div[1]/div/a//@href')
    # temp_manhua_name_List = etree.HTML(rs.text).xpath('/html/body/div[2]/div[1]/div/a/img//@alt')
    if list_content:
        tb = pt.PrettyTable()
        tb.field_names = ["序号", "漫画名","目录链接"]
        for index, list_content_item in enumerate(list_content):
            tb.add_row([index, nameList[index]['alt'].strip(), 'https://www.mkzhan.com'+list_content_item['href']])
        print(tb)
        print('请选择你要下载的漫画序号，请输入数字，请不要输入其他字符，也不要输入超过最大序号的字符')
        user_choice = int(input())
        catalogue_html_href = 'https://www.mkzhan.com'+list_content[user_choice]['href']
        global manhua_name
        manhua_name = validateTitle(nameList[user_choice]['alt'].strip())
        return catalogue_html_href
    else:
        return ''


if __name__ == '__main__':
    manhua_names = None
    chapter_url=get_manhua_inf()
    if chapter_url!='':
        manhua_url = chapter_url.strip()
        manhua_names = manhua_name.strip()
        # print(manhua_url)
        # print(manhua_names)
    else:
        print('未找到漫画资源')
    # cmdline.execute(str("scrapy crawl mkz_spiders -a manhua_url=%s -a manhua_names=%s"%(manhua_url,manhua_names)).split())

    spider = MkzSpidersSpider( manhua_url,manhua_names)
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider, manhua_url=manhua_url, manhua_names=manhua_names)  ## <-------------- (1)
    process.start()
