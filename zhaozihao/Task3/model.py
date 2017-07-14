#! /usr/bin/pythpn
# encoding:utf-8
from scrapy import cmdline
import web,re,urllib2,MySQLdb,time,hashlib,getopt
# 数据库连接
db=web.database(dbn='mysql',host='localhost',port=3306,db='python',user='root',pw='root',charset='utf8')

def create_md5(str):#获取字符串生成md5
	md5=hashlib.md5()
	md5.update(str)
	return md5.hexdigest()

def get_users():#获取用户信息
	return db.select('blog_users',order='id')

def get_admin():#获取管理员信息
	return db.select('admin_users',order='id')

def change_admin(adminname,newpassword):#修改管理员密码
	return db.update('admin_users',where='username=$adminname',vars=locals(),password=create_md5(newpassword))

def new_users(username,password):#注册新用户
	db.insert('blog_users',username=username,password=create_md5(password))

def del_user(id):#删除用户
	db.delete('blog_users',where='id=$id',vars=locals())

def change_password(id,newpassword):#修改指定用户的密码
	db.update('blog_users',where='id=$id',vars=locals(),password=create_md5(newpassword))

def get_posts():#获取所有留言
    return db.select('blog',order='id')

def get_post(id):#获取留言内容
    try:
        return db.select('blog',where='id=$id',vars=locals())[0]
    except IndexError:
        return None

def new_post(author,title,text):#新建留言
    db.insert('blog',author=author,title=title,content=text,posted_on=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def del_post(id):#删除留言
    db.delete('blog',where='id=$id',vars=locals())

def update_post(id,author,title,text):#修改留言
    db.update('blog',where='id=$id',vars=locals(),author=author,title=title,content=text)

def CreateDatabase():#没有指定数据库和表则创建它
	try:
		conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='root')
		cur=conn.cursor()
		cur.execute('select * from information_schema.SCHEMATA where SCHEMA_NAME="python"')
		if cur.fetchone()==None:
			cur.execute('create database if not exists python DEFAULT CHARSET=utf8')
			conn.select_db('python')
		else:
			conn.select_db('python')
		cur.execute('select * from information_schema.TABLES where TABLE_NAME="blog"')
		if cur.fetchone()==None:
			cur.execute('create table if not exists blog(id INT AUTO_INCREMENT,author TEXT,title TEXT,content TEXT,posted_on DATETIME,PRIMARY KEY(id)) DEFAULT CHARSET=utf8')
		cur.execute('select * from information_schema.TABLES where TABLE_NAME="blog_users"')
		if cur.fetchone()==None:
			cur.execute('create table if not exists blog_users(id INT AUTO_INCREMENT,username TEXT,password TEXT,PRIMARY KEY(id)) DEFAULT CHARSET=utf8')
		cur.execute('select * from information_schema.TABLES where TABLE_NAME="admin_users"')
		if cur.fetchone()==None:
			cur.execute('create table if not exists admin_users(id INT AUTO_INCREMENT,username TEXT,password TEXT,PRIMARY KEY(id)) DEFAULT CHARSET=utf8')
			db.insert('admin_users',username='admin',password=create_md5('admin'))
		cur.close()
		conn.close()
	except:
		print "[CreateDatabase]警报：数据库没有正常工作！原因可能如下：".decode('utf-8')
		print "1.数据库没有打开或2.用户名、密码与设定不符，若是情况2，请手动修改代码".decode('utf-8')
		return False
	return True

class Tool: 
	BgnCharToNoneRex=re.compile("(\t|\n| |<a.*?>|<img.*?>)")    
	EndCharToNoneRex=re.compile("<.*?>")  
	BgnPartRex=re.compile("<p.*?>")  
	CharToNewLineRex=re.compile("(<br/>|</p>|<tr>|<div>|</div>)")  
	CharToNextTabRex=re.compile("<td>")    
	replaceTab=[("<","<"),(">",">"),("&","&"),("&","\""),(" "," ")]  
	def Replace_Char(self,rep_str):  
		rep_str=self.BgnCharToNoneRex.sub("",rep_str)  
		rep_str=self.BgnPartRex.sub("\n    ",rep_str)  
		rep_str=self.CharToNewLineRex.sub("\n",rep_str)  
		rep_str=self.CharToNextTabRex.sub("\t",rep_str)  
		rep_str=self.EndCharToNoneRex.sub("",rep_str)  
		for t in self.replaceTab: 
			rep_str=rep_str.replace(t[0],t[1])    
		return rep_str

class NetWorm_baidu:
	def __init__(self,url):    
		self.myUrl=url+'?see_lz=1'
		self.myTool=Tool()
		self.author="None"
		self.title="None"
		self.datas=[]
 
	def save_data(self,url,endPage):#输出内容  
		self.get_data(url,endPage)#加载页面数据到数组中

	def baidu_tieba(self):#初始化加载页面并将其转码储存  
		myPage=urllib2.urlopen(self.myUrl).read().decode("utf-8")#读取页面的原始信息并将其从gbk转码  
		endPage=self.page_counter(myPage)#计算楼主发布内容一共有多少页
		self.find_author(myPage)
		self.find_title(myPage)
		self.save_data(self.myUrl,endPage)#获取最终的数据

	def page_counter(self,myPage):#用来计算一共有多少页    
		myMatch=re.search(r'class="red">(\d+?)</span>',myPage,re.S)#匹配"共有<span class="red">12</span>页"来获取一共有多少页  
		if myMatch:    
			endPage=int(myMatch.group(1))  
		else:  
			endPage=0   
		return endPage  

	def find_author(self,myPage):#寻找该帖的作者
		myMatch=re.search(r'<div class="louzhubiaoshi  j_louzhubiaoshi" author="(.*?)">',myPage,re.S)
		if myMatch:
			self.author=myMatch.group(1)

	def find_title(self,myPage):#寻找该帖的标题   
		myMatch=re.search(r'<h3 class="core_title_txt pull-left text-overflow .*?>(.*?)</h3>',myPage,re.S)#匹配 <h3 class="core_title_txt" title="">xxxxxxxxxx</h3> 找出标题
		if myMatch:  
			self.title=myMatch.group(1)
  
	def get_data(self,url,endPage):#获取页面源码并将其存储到数组中  
		url=url+'&pn='  
		for i in range(1,endPage+1):#将myPage中的html代码处理并存储到datas里面 
			myPage=urllib2.urlopen(url+str(i)).read()    
			self.deal_data(myPage.decode('utf-8'))  

	def deal_data(self,myPage):#将内容从页面代码中抠出来
		myItems=re.findall('id="post_content.*?>(.*?)</div>',myPage,re.S)  
		for item in myItems:  
			data = self.myTool.Replace_Char(item.replace("\n","").encode('utf-8'))  
			self.datas.append(data+'\n')