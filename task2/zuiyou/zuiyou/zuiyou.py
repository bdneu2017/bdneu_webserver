#coding:utf-8
#使用火狐浏览器 默认路径安装
import scrapy
from selenium import webdriver
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')#避免ascii编码 错误  unicode解码错误

driver=webdriver.Firefox()

class ZuiyouSpider(scrapy.Spider):
	name='zuiyou'
	allowed_domains=['zuiyou.ixiaochuan.cn']
	start_urls=['https://zuiyou.ixiaochuan.cn/home']

	def parse(self,response):
		driver.get('https://zuiyou.ixiaochuan.cn/home')
		#driver.find_element_by_xpath('//span[text()="图文"]').click()		
		try:
			while True:
				f1=open('1.txt','w')
				f2=open('2.txt','w')				
				while True:
					try:
						driver.find_element_by_class_name('home-loadMore').click()
					except:
						break
					#driver.implicitly_wait(10)
				time.sleep(5)
				names=driver.find_elements_by_class_name('name')			
				for name in names:
					f1.write(name.text+'\n')
				titles=driver.find_elements_by_class_name('post-content')
				for title in titles:
					f2.write(title.text+'\n')	
				f1.close()
				f2.close()
				driver.refresh()  # 刷新
				time.sleep(5)
		except:	
			driver.quit()

	