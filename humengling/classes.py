# coding:utf-8
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









