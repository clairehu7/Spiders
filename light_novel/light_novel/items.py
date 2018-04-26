# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LightNovelItem(scrapy.Item):
    title = scrapy.Field()
    link_url = scrapy.Field()
    text = scrapy.Field()
    pass
