# coding:utf-8
from flask import Flask
from flask_babelex  import Babel  
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # 实例
babe = Babel(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/test'  # bind
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
db = SQLAlchemy(app)







