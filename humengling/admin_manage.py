# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from classes import User
from app import app, db
from words import Word, FilterWord,top_keys,AlertMail
from flask_login import current_user


class MyView1(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name=='Admin':
            return True
        return False
    #column_exclude_list=('password')
    column_labels=dict(username=u'用户名',password_md5=u'密码摘要',role=u'用户级别',word=u'留言')

class MyView2(ModelView):  
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name=='Admin':
            return True
        return False
    can_create=False
    column_labels=dict(time_now=u'时间',title=u'标题',content=u'内容',user=u'用户名')
class  FilterView(ModelView):
 	def is_accessible(self):
 		if current_user.is_authenticated and current_user.role.name=='Admin':
 			return True
 	column_labels=dict(key=u'关键字',times=u'出现次数',alert=u'是否告警（1：是 0：否）')
class TopKeyView(BaseView):
	def is_accessible(self):
		if current_user.is_authenticated and current_user.role.name=='Admin':
			return True
	@expose('/')
	def top_key(self):
		top_3=top_keys()
		return self.render('top_key.html',top_3=top_3)
class AlertMailView(ModelView):
	def is_accessible(self):
		if current_user.is_authenticated and current_user.role.name=='Admin':
			return True
	can_create=False
	column_labels=dict(mail=u'告警邮箱')

 		
admin=Admin(app,name=u'后台管理系统') 
admin.add_view(MyView1(User,db.session,name=u'管理账号')) 
admin.add_view(MyView2(Word,db.session,name=u'管理留言'))  
admin.add_view(FilterView(FilterWord,db.session,name=u'过滤关键字'))
admin.add_view(TopKeyView(name=u'关键字top3'))
admin.add_view(AlertMailView(AlertMail,db.session,name=u'告警邮箱配置'))







