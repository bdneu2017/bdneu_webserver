# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from classes import User
from app import app,db
from words import Word
admin=Admin(app,name=u'后台管理系统') 
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

admin.add_view(MyView1(User,db.session,name=u'管理账号')) 
admin.add_view(MyView2(Word,db.session,name=u'管理留言'))  







