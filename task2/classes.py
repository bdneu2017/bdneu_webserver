# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin,current_user
from app import app,db
import time

class Role(db.Model):  # 角色 管理员或者普通用户
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    user = db.relationship('User',backref='role')
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def __repr__(self):
        return '%s' % self.name

class User(db.Model,UserMixin):  # 注册用户
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_md5 = db.Column(db.String(35),nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=False)  
    word = db.relationship('Word',backref='user') 
    
    def __init__(self,username='',password_md5='',role_id=None):
        self.username=username
        self.password_md5=password_md5
        self.role_id=role_id
    def __repr__(self):
        return '%s' % self.username


class Word(db.Model):  #用户留言
    __tablename__='words'
    id=db.Column(db.Integer,primary_key=True)
    time_now=db.Column(db.String(20))
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
 
    def __init__(self,title,content,user_id):
        self.title=title
        self.content=content
        self.user_id=user_id
        self.time_now=str(time.strftime('%Y-%m-%d %H:%M:%S'))

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






