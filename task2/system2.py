# coding:utf-8
from login import login_manager
from flask import render_template
from login import login,logout,verify #登入登出验证
from words import words,update_words #
from register import register,update_register
from flask_admin import Admin
from classes import MyView1,MyView2,User,Word
from app import app,db
import sys
reload(sys)
sys.setdefaultencoding('utf8')

admin=Admin(app,name=u'后台管理系统') 
admin.add_view(MyView1(User,db.session,name=u'管理账号')) 
admin.add_view(MyView2(Word,db.session,name=u'管理留言'))  

@login_manager.user_loader
def load_user(userid):
    user=User.query.get(userid)
    return user
#主页
@app.route('/')
def home():
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)