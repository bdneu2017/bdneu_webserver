# _*_ coding: utf-8 _*_
'''
#调试模式是否开启
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#mysql数据库连接信息,这里改为自己的账号
SQLALCHEMY_DATABASE_URI = "mysql://username:password@ip:port/dbname"
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))
FILEDIR = os.path.join(basedir,'blog2/upload')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog2/flaskr.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'