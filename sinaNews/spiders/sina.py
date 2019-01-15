# -*- coding: utf-8 -*-
import scrapy
import os
import  re
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
        #meta数据，此处保存parse的item
        meta_1=response.meta['meta_1']

        #按我的想法就是先把所有的找出来，访问一遍看看符不符合文章格式
        sonUrls = response.xpath('//a/@href').extract()

        items=[]

        for i in range(0,len(sonUrls)):
            item = SinanewsItem()
            item['parentTitle'] = meta_1['parentTitle']
            item['parentUrl'] = meta_1['parentUrl']
            item['subUrl'] = meta_1['subUrl']
            item['subTitle'] = meta_1['subTitle']
            item['subFilename'] = meta_1['subFilename']
            item['sonUrl'] = sonUrls[i]
            # items.append(item)
            yield item

        # for item in items:
        #     yield scrapy.Request(url=item['sonUrl'], meta={'meta_2': item}, callback=self.detail_parse)

    # 数据解析方法，获取文章标题和内容,验证一下格式，可能不是正文链接
    def detail_parse(self, response):
        head=response.xpath('//h1[@class="main-title"]/text()')
        if len(head)>0 :
            print head.extract()[0]
            item=response.meta['meta_2']
            content=""
            content_list=response.xpath('//div[id=@"artibody"]/p/text()').extract()
            for one in content_list:
                content+=one
            item['head']=head
            item['content']=content
            yield item