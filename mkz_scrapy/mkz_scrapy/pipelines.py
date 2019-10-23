# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests

class MkzScrapyPipeline(object):

    def process_item(self, item, spider):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'cookie': 'UM_distinctid=16706eb86dcd8-02bc2f02cd5057-333b5602-100200-16706eb86dd6e5; bdshare_firstime=1542009358470; laravel_session=eyJpdiI6InJZMTQrZFlRVFphOVlXU2R0dFwvRnl3PT0iLCJ2YWx1ZSI6IjFJZGdacHA5YkJSRzhHSWJoVklwaTNiaTl0dHRCMzFwSzRGT0oxWm81MXl5aGtkT0lDVHFQRTlBcUJkN3hEQ2xWXC9yZWRxbjJzNSthVWg2VFBVbXRUZz09IiwibWFjIjoiZmZiY2Q0YjkyZTAwMzBjNDk4YjAwZmVkYTg1NzY3NmY4MzU5YjM2NjQzZTdlNTExMWI3ZmJiYTMyNjhlN2YwMSJ9; CNZZDATA1255781707=1633799429-1542006327-%7C1542011727; CNZZDATA1000465408=1899900830-1542005345-%7C1542012974',
            'referer': 'https://m.dmzj.com/info/zuizhongwochengleni.html'
        }

        #path是下载的地址，这里设定的是e盘根目录
        path = 'e:/'

        #确认漫画的目录是否存在
        manhua_name = os.path.join(path,item['big_title'])
        # print(manhua_name)
        if not os.path.exists(manhua_name):
            os.mkdir(manhua_name)
        # 确认每一话的目录是否存在
        catapot_name = os.path.join(manhua_name,item['title'])
        if not os.path.exists(catapot_name):
            os.mkdir(catapot_name)
        #开始逐一下载一话中所有的图片
        #capter为该话中图片的具体名字
        capter=0
        for pic_url in item['pic_urls']:
            capter=capter+1
            response = requests.get(pic_url, headers=headers).content
            with open(catapot_name+r'\\'+str(capter)+".jpg",'wb') as fp:
                fp.write(response)
                fp.close()
                print("正在下载"+item['big_title']+" "+item['title']+" "+str(capter))
        return item