# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
XML_NAME='option.xml'#操作的xml文件名

class OptionInXML:#读取和修改xml文件(用于设定爬虫爬取对象及爬取内容规则)
	def GetOption(self,option_name):#输出相应属性的值
		global XML_NAME
		tree = ET.parse(XML_NAME)
		root = tree.getroot()
		for child in root:
			if child.get('name')==option_name:
				return child.text
		print "AttributeError:this attribute is not exist"
		return None

	def SetOption(self,option_name,new_option):#修改xml中的设置，成功返回true
		global XML_NAME
		tree = ET.parse(XML_NAME)
		root = tree.getroot()
		for child in root:
			if child.get('name')==option_name:
				child.text=new_option
				tree.write(XML_NAME)
				print "this attribute change successful"
				return True
		print "AttributeError:this attribute is not exist"
		return False
		
if __name__=='__main__':#测试用
	test=OptionInXML()
	print test.GetOption('child_page')