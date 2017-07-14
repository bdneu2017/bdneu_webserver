# -*- coding: utf-8 -*-
from scrapy import cmdline    
import sys,getopt,MySQLdb

def StartSpider():#启动爬虫，需带参数-u 目标url
	str="scrapy crawl Page_Spider -a target_url="#爬虫启动命令
	try:
		options,args=getopt.getopt(sys.argv[1:],"u:",["url="])#获取程序运行参数
	except:
		print "Error:Need Target URL"
		sys.exit()
	for name,value in options:
		if name in ("-u","--url"):
			url=str+value
	cmdline.execute(url.split())

if __name__=='__main__':
	StartSpider()