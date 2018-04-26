# -*- coding: utf-8 -*-

# Scrapy settings for light_novel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'light_novel'

SPIDER_MODULES = ['light_novel.spiders']
NEWSPIDER_MODULE = 'light_novel.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# DOWNLOAD_DELAY = 0.25
ITEM_PIPELINES = {
    'light_novel.pipelines.LightNovelPipeline': 300,
}

