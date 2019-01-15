# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def __init__(self):
        self.filename=open("url.txt","w")

    def process_item(self, item, spider):
        sonUrl=item['sonUrl']
        sonUrl+='\n'
        self.filename.write(sonUrl.encode("utf-8"))
        self.filename.flush()
        return item

    def close_spider(self,spider):
        self.filename.close()
