# -*- coding: UTF-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from work.items import Page_SpiderItem
from work.model import OptionInXML
import sys
import scrapy
import getopt
reload(sys)
sys.setdefaultencoding("utf-8")

headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
option=OptionInXML()#初始化操作xml文件的实例，类有两个方法，得到属性GetOption(option_name)和修改属性SetOption(option_name,value)

class PageSpider(CrawlSpider):
	name="Page_Spider"
	download_delay=2  #爬虫每次爬取延迟2秒
	
	rules = (#使用rule完成翻页和爬取主页面内子页面的功能
		Rule(SgmlLinkExtractor(allow=(option.GetOption('next_page'),)),),
		Rule(SgmlLinkExtractor(allow=(option.GetOption('child_page'),)),callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=(option.GetOption('other_child_page'),)),callback='parse_item'),
		)

	def __init__(self,target_url,*args,**kwargs):#初始化设置爬虫属性，读取爬虫的域和起始url
		global option
		self.allowed_domains=[option.GetOption('domain')]#读取爬虫的基本设置
		super(PageSpider,self).__init__(*args,**kwargs)
		self.start_urls=[target_url]
	
	def parse_item(self,response):#爬取指定内容并交给pipelines处理,暂时只收集标题、作者、内容
		global option
		sel=Selector(response)   
		item=Page_SpiderItem()
		title=sel.xpath(option.GetOption('title_pattern')).extract()
		item['title']=[n.encode('utf-8') for n in title]
		author=sel.xpath(option.GetOption('author_pattern')).extract()
		item['author']=[n.encode('utf-8') for n in author]
		content=sel.xpath(option.GetOption('content_pattern')).extract()
		item['content']=[n.replace(' ','').encode('utf-8') for n in content]
		yield item