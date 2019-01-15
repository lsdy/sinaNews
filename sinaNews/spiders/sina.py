# -*- coding: utf-8 -*-
import scrapy
import os
from sinaNews.items import SinanewsItem


class SinaSpider(scrapy.Spider):
    # Spider的名字，运行命令时根据名字选择启动的spider
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items=[]

        for each in response.xpath('//div[@id="tab01"]/div'):
            #获得大标题
            #地方站没有内容，考虑下爬不爬
            parentTitleObject=each.xpath('./h3/a/text()').extract()
            if(len(parentTitleObject)==0):
                continue
            parentTitle=parentTitleObject[0]
            parentUrl=each.xpath('./h3/a/@href').extract()[0]

            subTitles=each.xpath('./ul/li/a/text()').extract()
            subUrls = each.xpath('./ul/li/a/@href').extract()

            parentFilename = "./Data/" + parentTitle
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)
            for j in range(0,len(subUrls)):
                subFilename=parentFilename+'/'+subTitles[j]
                # 如果目录不存在，则创建目录
                if (not os.path.exists(subFilename)):
                    os.makedirs(subFilename)

                item=SinanewsItem()

                item['parentTitle']=parentTitle
                item['parentUrl']=parentUrl

                item['subUrl']=subUrls[j]
                item['subTitle']=subTitles[j]
                item['subFilename'] = subFilename
                items.append(item)
                pass
        for item in items:
            yield scrapy.Request(url=item['subUrl'],meta={'meta_1':item},callback=self.second_parse)

    #对于返回的小类的url，再进行递归请求
    def second_parse(self, response):

        meta_1=response.meta['meta_1']
        
        pass