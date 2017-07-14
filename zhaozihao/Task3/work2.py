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
		posts=model.get_posts()
		return render.index(posts)

	def POST(self):
		flag_loginfail=1
		posts=model.get_posts()
		login_user=model.get_users()
		for user in login_user:
			if web.input().login_username==user.username and model.create_md5(web.input().login_password)==user.password:
				flag_loginfail=0
				web.setcookie('username',web.input().login_username)
		if flag_loginfail:
			return render.index(posts)
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

class Backstage:#后台管理界面类
	def GET(self):
		posts=model.get_posts()
		return render.backstage(posts)

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
		os.system('python main.py -u '+'"'+start_url+'"')
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

class Logout:# 退出登录
    def GET(self):
        web.setcookie('username','',expires=-1)
        raise web.seeother('/')

def notfound():# 定义404
    return web.notfound("sorry,the page you were looking for was not found")
app.notfound=notfound

class ExitServer:
	def GET(self):
		print "\n---服务器已正常停止工作---".decode('utf-8')
		time.sleep(0.5)
		sys.exit()


if __name__ == '__main__':#运行
	if model.CreateDatabase()==True:
		app.run()
	else:
		print "\n程序异常，请按照报错内容完成准备工作再尝试运行".decode('utf-8')

