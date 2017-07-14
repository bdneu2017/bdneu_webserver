# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Page_SpiderItem(scrapy.Item):#存储内容的容器
	title=scrapy.Field()
	author=scrapy.Field()
	content=scrapy.Field()