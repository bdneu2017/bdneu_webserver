#! /usr/bin/python
# encoding:utf-8

import web,model,sys,time,os
from xml.etree import ElementTree as ET
XML_NAME='option.xml'#操作的xml文件名

urls = (# url映射
    '/','Index',#主页
    '/backstage','Backstage',#后台主页，需修改
    '/admin','Admin',#管理员登录页,初始管理员用户名admin,密码admin
    '/usercontrol','UserControl',#用户控制页，未完成
    '/deleteuser/(\d+)','DeleteUser',#删除用户
    '/change/(\d+)','ChangePassword',#更改指定用户的密码
    '/changeadmin','ChangeAdmin',#修改管理员密码
    '/networm','NetWorm_getbaidu',#爬虫，抓取百度贴吧的指定帖子
    '/networm_plus','NetWorm_plus',#爬虫，scrapy加强版
    '/change_xml','Change_xml',#修改Scrapy爬虫设置文件
    '/adduser','AddUser',#管理员添加用户
    '/new', 'New',#新发布文章
    '/delete/(\d+)', 'Delete',#删除文章
    '/edit/(\d+)', 'Edit',#修改文章
    '/logout', 'Logout',#退出登录
    '/register','Register',#注册用户
    '/exitserver','ExitServer',#停止服务器程序
    '/keyword','KeyWord',#关键字过滤设置
    '/addkeyword','AddKeyWord',#添加关键字
    '/editkw/(\d+)','EditKW',#修改关键字
    '/deletekw/(\d+)','DeleteKW',#删除关键字
    '/chatroom','ChatRoom',#在线聊天室
    '/chatstart','ChatStart',#启动聊天服务器
    '/mailoption','MailOption',#打开/关闭发送邮件报警功能
    '/optionclear','OptionClear',#如果打开了邮件报警功能又未输入报警邮件信息，则自动关闭该功能
)

app=web.application(urls,globals())

t_globals = {# 模板公共变量
    'datestr': web.datestr,
    'cookie': web.cookies,
}
# 指定模板目录，并设定公共模板
render=web.template.render('templates',base='base',globals=t_globals)

class Index:#登录类
	def GET(self):
		refunc=model.ReplaceKeyword()
		posts=model.get_posts()
		return render.index(posts,refunc)

	def POST(self):
		flag_loginfail=1
		refunc=model.ReplaceKeyword()
		posts=model.get_posts()
		login_user=model.get_users()
		for user in login_user:
			if web.input().login_username==user.username and model.create_md5(web.input().login_password)==user.password:
				flag_loginfail=0
				web.setcookie('username',web.input().login_username)
		if flag_loginfail:
			return render.index(posts,refunc)
		raise web.seeother('/')

class Register:#注册用户类
	def GET(self):
		return render.register()

	def POST(self):
		if web.input().reg_password1==web.input().reg_password2:
			model.new_users(web.input().reg_username,web.input().reg_password1)
		else:
			return render.register()
		raise web.seeother('/')

class Admin:#管理员类	
	def GET(self):
		return render.admin()
		
	def POST(self):
		admin_users=model.get_admin()
		for user in admin_users:
			if web.input().admin_username==user.username and model.create_md5(web.input().admin_password)==user.password:
				web.setcookie('username',web.input().admin_username)
		raise web.seeother('/admin')

mail_info={'send_to':0,'stmp_server':0,'username':0,'password':0,'flag':0}

class Backstage:#后台管理界面类
	def GET(self):
		refunc=model.ReplaceKeyword()
		posts=model.get_posts()
		if mail_info['flag']==1:
			key_temp=model.sel_keyword()
			count=model.count_keyword()
			for list in key_temp:
				for n in count:
					if count[n]>0 and n==list.keyword:
						if list.option==0:
							continue
						else:
							model.send_mail(mail_info['send_to'],"Warning:Find Keyword"+n,"留言中发现目标关键字："+n,mail_info['stmp_server'],mail_info['username'],mail_info['password'],mail_info['username'],mail_info['username'])
							break
		return render.backstage(posts,refunc)

class MailOption:#设置报警邮件
	def GET(self):
		if mail_info['flag']==0:
			mail_info['flag']=1
			return render.mainoption()
		else:
			mail_info['flag']=0
			raise web.seeother('/keyword')

	def POST(self):
		mail_info['send_to']=web.input().send_to
		mail_info['stmp_server']=web.input().stmpsever
		mail_info['username']=web.input().username
		mail_info['password']=web.input().password
		raise web.seeother('/keyword')

class OptionClear:#如果打开了邮件报警功能又未输入报警邮件信息，则自动关闭该功能
	def GET(self):
		mail_info['flag']=0	
		raise web.seeother('/keyword')

class UserControl:#用户管理类
	def GET(self):
		userlists=model.get_users()
		return render.usercontrol(userlists)

class AddUser:#管理员添加新用户
	def GET(self):
		return render.adduser()
			
	def POST(self):
		model.new_users(web.input().add_username,web.input().add_password)
		raise web.seeother('/usercontrol')

class ChangeAdmin:#修改管理员密码
	def GET(self):
		return render.changeadmin()

	def POST(self):
		if web.input().new_adminpassword==web.input().new_adminpassword2:
			model.change_admin('admin',web.input().new_adminpassword)
		raise web.seeother('/backstage')

class ChangePassword:#修改用户密码	
	def GET(self,id):
		return render.change()
		
	def POST(self,id):
		if web.input().new_password1==web.input().new_password2:
			model.change_password(int(id),web.input().new_password1)
		raise web.seeother('/usercontrol')

class DeleteUser:#删除用户
	def GET(self,id):
		model.del_user(int(id))
		raise web.seeother('/usercontrol')

class NetWorm_getbaidu:#爬虫-百度贴吧
	def GET(self):
		return render.networm()

	def POST(self):
		bdurl=str(web.input().tiebaurl)
		worm=model.NetWorm_baidu(bdurl)
		worm.baidu_tieba()
		str_content=('').join(worm.datas)
		model.new_post(worm.author,worm.title,str_content)
		raise web.seeother('/backstage')

class NetWorm_plus:#爬虫-Scrapy
	def GET(self):
		return render.networm_plus()
	
	def POST(self):
		start_url=str(web.input().starturl)
		os.system('python spider.py -u '+'"'+start_url+'"')
		raise web.seeother('/backstage')

class Change_xml:#修改Scrapy爬虫设置
	def GET(self):
		global XML_NAME
		tree = ET.parse(XML_NAME)
		root = tree.getroot()
		return render.change_xml(root)

	def POST(self):
		global XML_NAME
		tree = ET.parse(XML_NAME)
		root = tree.getroot()
		root[0].text=web.input().domain
		root[1].text=web.input().next_page
		root[2].text=web.input().child_page
		root[3].text=web.input().other_child_page
		root[4].text=web.input().title_pattern
		root[5].text=web.input().author_pattern
		root[6].text=web.input().content_pattern
		tree.write(XML_NAME)
		raise web.seeother('/networm_plus')

class KeyWord:#管理关键字
	def GET(self):
		count=model.count_keyword()
		dict=sorted(count.items(),key=lambda d:d[1],reverse=True)
		key_w=model.sel_keyword()
		return render.keyword(key_w,count,dict)

class AddKeyWord:#添加关键字
	def GET(self):
		return render.addkeyword()
	
	def POST(self):
		model.new_keyword(web.input().newkeyword,web.input().alert_mail)
		raise web.seeother('/keyword')

class EditKW:#修改关键字
	def GET(self,id):
		keywd=model.get_keyword(int(id))
		return render.editkw(keywd.keyword)
	
	def POST(self,id):
		model.update_keyword(int(id),web.input().newkeyword,web.input().alert_mail)
		raise web.seeother('/keyword')		

class DeleteKW:# 删除关键字
    def GET(self,id):
        model.del_keyword(int(id))
        raise web.seeother('/keyword')		

class New:# 新建留言类
    def GET(self):
        return render.new()

    def POST(self):
		model.new_post(web.cookies().get('username'),web.input().post_title,web.input().post_text)
		raise web.seeother('/')

class Delete:# 删除留言类
    def GET(self,id):
        model.del_post(int(id))
        if web.cookies().get('username')=='admin':
            raise web.seeother('/backstage')
        else:
            raise web.seeother('/')

class Edit:# 编辑留言类
    def GET(self,id):
        post=model.get_post(int(id))
        return render.edit(post)

    def POST(self,id):
        post=model.get_post(int(id))
        model.update_post(int(id),web.input().post_author,web.input().post_title,web.input().post_text)
        if web.cookies().get('username')=='admin':
            raise web.seeother('/backstage')
        else:
            raise web.seeother('/')

class ChatRoom:#在线聊天系统
	def GET(self):
		return render.chatroom()

class ChatStart:#启动聊天服务器
	def GET(self):
		server=model.websocket_server(9000)
		server.start()
		raise web.seeother('/backstage')
			

class Logout:# 退出登录
    def GET(self):
        web.setcookie('username','',expires=-1)
        raise web.seeother('/')

def notfound():# 定义404
    return web.notfound("sorry,the page you were looking for was not found")
app.notfound=notfound

class ExitServer:#关闭网站服务器
	def GET(self):
		print "\n---服务器已正常停止工作---".decode('utf-8')
		time.sleep(0.5)
		sys.exit()


if __name__ == '__main__':#运行
	if model.CreateDatabase()==True:
		app.run()
	else:
		print "\n程序异常，请按照报错内容完成准备工作再尝试运行".decode('utf-8')

