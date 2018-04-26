# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from light_novel.items import LightNovelItem

# http://m.webqxs.com/0/42/
# http://m.webqxs.com/0/42/5678.html

# 设置要爬的开始章节和结束章节
global start_index,end_index
start_index = 1
end_index = 10

global end_url,current_index
end_url = ''
current_index = 0

class StorySpider(scrapy.Spider):

    if start_index > end_index:
        raise ValueError('start_index > end_index!')
    if start_index < 1:
        raise  ValueError('start_index at least is 1')

    global current_index
    current_index = start_index

    name = 'story'

    def __init__(self):
        # server 域名
        self.server_link = 'http://m.webqxs.com'
        self.allowed_domains = ['m.webqxs.com']
        # http://m.webqxs.com/0/42_2/
        self.start_urls = ['http://m.webqxs.com/0/42/']

    # 从 start_requests 发送请求
    def start_requests(self):
        yield scrapy.Request(url = self.start_urls[0], callback = self.parse1)

    # 解析 response,获得章节链接地址
    def parse1(self, response):

        # 得到目录第一页的 li 个数
        lis = response.xpath("//ul[@class='chapters']/li").extract()

        global start_index,end_index
        if len(lis) < start_index:
            next_url = response.xpath("//div/a[text() ='下一页']/@href").extract()[0]
            next_url = self.server_link + next_url
            if next_url == '':
                raise ValueError('no next_url, check start_index')
                return
            # 此时 start_index 应调整为当前目录页的 li 的位置，end_index 也要相应调整
            start_index = start_index - len(lis)
            end_index = end_index - len(lis)
            yield scrapy.Request(url=next_url, callback=self.parse1)
            return

        # 得到的数组 要取[0]
        first_index = str(start_index + 1)
        first_url = response.xpath('//ul/li['+ first_index + ']/a/@href').extract()[0]

        # 保存第一章的链接地址 到在 items.py 定义的 link_url
        item = LightNovelItem()
        item['link_url'] = first_url

        urls = response.xpath('//ul/li/a/@href').extract()

        global end_url
        if end_index < len(urls):
            end_url = urls[end_index]
        else:
            # 网页开 http://m.webqxs.com/0/42/ 查看最后一章，会发现它的"下一章"链接指回目录，
            # 所以如果读取到 下一章 的链接为目录，就说明这一章已经是最后一章
            end_url = "http://m.webqxs.com/0/42/"

        # 根据章节链接，发送 Request 请求，并传递 item 参数
        yield scrapy.Request(url = item['link_url'], meta = {'item':item,}, callback = self.parse_article)

    def parse_article(self, response):
        item = response.meta['item']

        # 章节名,取元素
        title = response.xpath("//h1[@id='chaptertitle']/text()").extract()[0]
        item['title'] = title

        print("title is  ", title)

        # 文章，for in 取元素，存到字符串里
        details = response.xpath('//p/text()').extract()
        s = ''
        for detail in details:
            s = s + detail + "\n\n"
        s = s.replace('切换语言[采用cookies记录/时效1天]：','')
        item['text'] = s

        # 下一章链接，取元素后拼接 host
        next_url = response.xpath("//ul/li/p[@class='p1 p3']/a/@href").extract()[0]
        next_url = self.server_link + next_url
        item['link_url'] = next_url

        global current_index
        current_index = current_index + 1
        print('current_index:   ',current_index)

        # 下一章链接为 end_url 时，不再请求
        # 下一章链接为空时，不再请求
        global end_url
        if next_url == end_url:
            yield item
        elif next_url == "":
            yield item
        else:
            yield item
            yield scrapy.Request(url=item['link_url'], meta={'item': item}, callback=self.parse_article)