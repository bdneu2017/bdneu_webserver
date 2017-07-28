# coding:utf-8
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from app import db


class Role(db.Model):  # 角色: 管理员或者普通用户
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship('User', backref='role')  # 角色表与用户表之间是一对多的关系

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '%s' % self.name  # 后台显示


class User(db.Model, UserMixin):  # 注册用户
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    word = db.relationship('Word', backref='user')  # 用户表和留言表之间是一对多的关系

    @property
    def password(self):
        raise AttributeError('password is not readable')  # 密码只写不能读

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __init__(self, username='', password='', role_id=None):  # problem
        # 初始化后 后台创建内容才能正确使用
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role_id = role_id

    def __repr__(self):
        return '%s' % self.username









