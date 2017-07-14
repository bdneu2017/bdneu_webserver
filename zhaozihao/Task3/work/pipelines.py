# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,codecs,web,time

class Page_SpiderPipeline(object):#处理抓取内容，创建txt文件分别存储每一页的内容
	def process_item(self,item,spider):
		content='@:'
		author=''
		for i in item['author']:
			author+='@'+i+','
		for j in item['title']:
			title=j
		for k in item['content']:
			content+=k.replace(' ','')
		db=web.database(dbn='mysql',host='localhost',port=3306,db='python',user='root',pw='root',charset='utf8')
		posted_on=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		db.insert('blog',author=author,title=title,content=content,posted_on=posted_on)
		return item