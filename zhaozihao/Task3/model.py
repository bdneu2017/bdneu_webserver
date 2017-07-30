#! /usr/bin/pythpn
# encoding:utf-8
from scrapy import cmdline
import web,re,urllib2,MySQLdb,time,hashlib,getopt,socket,threading,base64
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

def sel_keyword():#获取关键字列表
	return db.select('keyword',order='id')

def new_keyword(keyword,option):#新建关键字
    db.insert('keyword',keyword=keyword,option=option)

def get_keyword(id):#获取指定关键字
    try:
        return db.select('keyword',where='id=$id',vars=locals())[0]
    except IndexError:
        return None

def count_keyword():#关键字计数
	keywords=[]
	posts_temp=[]
	dict={}
	kw=sel_keyword()
	posts=get_posts()
	for k in kw:
		keywords.append(k.keyword)
	for post in posts:
		posts_temp.append(post.content)	
	for i in keywords:
		count=0
		for j in posts_temp:
			count+=len(re.findall(i,j))
		dict[i]=count
	return dict

def update_keyword(id,keyword,option):#修改关键字
    db.update('keyword',where='id=$id',vars=locals(),keyword=keyword,option=option)

def del_keyword(id):#删除关键字
    db.delete('keyword',where='id=$id',vars=locals())

class ReplaceKeyword:#过滤替换关键字
	def __init__(self):
		self.keywords=[]
		self.values=[]
		lists=sel_keyword()
		for list in lists:
			self.keywords.append(list.keyword)
			self.values.append("***")
	
	def multiple_replace(self,text):
		adict=dict(zip(self.keywords,self.values))
		rx=re.compile('|'.join(map(re.escape,adict)))
		def one_xlat(match):
			return adict[match.group(0)]
		return rx.sub(one_xlat,text)

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
		cur.execute('select * from information_schema.TABLES where TABLE_NAME="keyword"')
		if cur.fetchone()==None:
			cur.execute('create table if not exists keyword(id INT AUTO_INCREMENT,keyword TEXT,option TEXT,PRIMARY KEY(id)) DEFAULT CHARSET=utf8')
		cur.close()
		conn.close()
	except:
		print "[CreateDatabase]警报：数据库没有正常工作！原因可能如下：".decode('utf-8')
		print "1.数据库没有打开或2.用户名、密码与设定不符，若是情况2，请手动修改代码".decode('utf-8')
		return False
	return True

class Tool:#百度贴吧爬虫-替换工具
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

class NetWorm_baidu:#百度贴吧爬虫
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

def send_mail(send_to,subject,body,smtp_server,username,password,cc=None,bcc=None):
    try:
        web.config.smtp_server='smtp.'+smtp_server   ##邮件发送服务器
        web.config.smtp_port=25    ##不设置将使用默认端口
        web.config.smtp_username=username   ##邮件服务器的登录名
        web.config.smtp_password=password   ##邮件服务器的登录密码
        web.config.smtp_starttls=True
        send_from=username   ##发送的邮件
        web.sendmail(send_from,send_to,subject,body,cc=cc,bcc=bcc)
        return 1  #pass
    except Exception,error:
        print error
        return -1 #fail		

global clients#存放客户端线程数据
clients={}

#通知客户端
def notify(message):
	for connection in clients.values():
		connection.send('%c%c%s' %(0x81,len(message),message))

#客户端处理线程
class websocket_thread(threading.Thread):
    def __init__(self,connection,username):#初始化连接套接字和用户名字
        super(websocket_thread, self).__init__()
        self.connection=connection
        self.username=username
    
    def run(self):#客户端与服务器建立连接
        print 'new client joined!'
        recvbuf=self.connection.recv(1024)
        headers=self.parse_headers(recvbuf)
        token=self.generate_token(headers['Sec-WebSocket-Key'])
        self.connection.send('\HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
								Upgrade: WebSocket\r\n\
								Connection: Upgrade\r\n\
								Sec-WebSocket-Accept: %s\r\n\r\n' % token
								)
        while True:
            try:
                recvbuf=self.connection.recv(1024)
            except socket.error,error:#客户端断开连接
                print "unexpected error:client close conneion",error
                clients.pop(self.username)
                break
            recvbuf=self.parse_data(recvbuf)
            if len(recvbuf)==0:
                continue
            message=self.username+": "+recvbuf
            notify(message)
            
    def parse_data(self,message):#处理数据
        v=ord(message[1])&0x7f
        if v==0x7e:
            p=4
        elif v==0x7f:
            p=10
        else:
            p=2
        mask=message[p:p+4]
        data=message[p+4:]
        return ''.join([chr(ord(v)^ord(mask[k%4])) for k,v in enumerate(data)])
        
    def parse_headers(self,message):#处理发送信息的头部
        headers={}
        header,data=message.split('\r\n\r\n',1)
        for line in header.split('\r\n')[1:]:
            key,value=line.split(': ',1)
            headers[key]=value
        headers['data']=data
        return headers

    def generate_token(self,message):#生成websocket连接用的key
        key=message+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ser_key=hashlib.sha1(key).digest()
        return base64.b64encode(ser_key)

#服务端
class websocket_server(threading.Thread):#服务端程序，建立套接字并等待连接
    def __init__(self,port):
        super(websocket_server,self).__init__()
        self.port=port

    def run(self):
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('127.0.0.1',self.port))
        sock.listen(10)
        print 'Server started!'
        while True:
            connection,address=sock.accept()
            try:
                username="ID"+str(address[1])
                thread=websocket_thread(connection,username)
                thread.start()
                clients[username]=connection
            except socket.timeout:
                print 'Connection timeout!'

if __name__=="__main__":#测试模块
	send_to = ['someone']     
	subject = '邮件标题'  
	body = '邮件内容\n可以有回车'  
	cc = ['someone']   ##抄送  
	bcc = ['someone']  ##密抄
	send_mail(send_to,subject,body,'someone','someone','someone',cc,bcc)