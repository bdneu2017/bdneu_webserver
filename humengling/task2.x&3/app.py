# coding:utf-8
from flask import Flask
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # 实例
babe = Babel(app)  # 中文化
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://root:123456@127.0.0.1:3306/test'
# 绑定 需要修改 数据库可能不存在
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'  # 中文化
app.secret_key = \
    's\x9e\xb0M\x860\xcf\xdb\xd7eR4J\xee\xf4\x1e\xe1\xccd\xfa\xcc\xbe\xd6u'
db = SQLAlchemy(app)
