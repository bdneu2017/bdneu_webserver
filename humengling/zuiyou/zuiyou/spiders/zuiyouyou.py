#coding:utf-8
#使用火狐浏览器 默认路径安装
#相关页面的url都是一样的，未用item
import scrapy
from selenium import webdriver
#from zuiyou.items import ZuiyouItem
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')#避免ascii编码 错误  unicode解码错误

class ZuiyouSpider(scrapy.Spider):
	name='zuiyou'
	allowed_domains=['zuiyou.ixiaochuan.cn']
	start_urls=['https://zuiyou.ixiaochuan.cn/home']	

	def parse(self,response):		
		driver=webdriver.PhantomJS()
		driver.get('https://zuiyou.ixiaochuan.cn/home')

		try:
			while True:
				#time.sleep(5)
				f1=open('1.txt','w+')
				thing=driver.find_elements_by_class_name("item")
				for t in thing:
					print t.text
					if t.text=="推荐":
						driver.find_element_by_xpath('//span[text()="推荐"]').click()
						f1.write("..................>^<推荐>^<.................\n")
					if t.text=="视频":
						driver.find_element_by_xpath('//span[text()="视频"]').click()
						f1.write("..................>^<视频>^<.................\n")
					if t.text=="图文":
						driver.find_element_by_xpath('//span[text()="图文"]').click()
						f1.write("..................>^<图文>^<.................\n")
					#driver.find_element_by_xpath('//span[text()=t.text]').click() # 为啥这样找不到元素
					time.sleep(3)
					while True:
						try:
							driver.find_element_by_class_name('home-loadMore').click()
						except:
							break
					time.sleep(3)
					mains=driver.find_elements_by_class_name('post-main')
					for main in mains:
						name=main.find_element_by_class_name('name')
						review=main.find_element_by_class_name('review')
						f1.write(name.text+': '+review.text+'\n')

				f1.close()
				f3=open('3.txt','w')
				f1=open('1.txt')		
				f3.write(f1.read())
				f1.close()
				f3.close()
				time.sleep(50)
				break
		finally:
			driver.quit()

	