# coding:utf-8
from app import app
from flask import render_template,flash,request,redirect,url_for
from flask_login import LoginManager,login_user, logout_user
from classes import User
from md5 import to_md5

app.secret_key='s\x9e\xb0M\x860\xcf\xdb\xd7eR4J\xee\xf4\x1e\xe1\xccd\xfa\xcc\xbe\xd6u'
login_manager=LoginManager(app)
login_manager.session_protection='strong'#cookie篡改时session被删除
login_manager.login_view='/'#重定向到主页
login_manager.login_message=u'请登录后访问'#自定义闪现消息
login_manager.login_message_category='info'

@app.route('/login', methods=['GET','POST'])  # 登录页面
def login():
    return render_template('login.html')

@app.route('/verify', methods=['GET','POST'])  # 验证 登入
def verify():#验证
    if request.method=='GET':
        flash(u'参数错误，请输message入账号密码后提交')       
    if request.method=='POST':
        tuser=request.form['username']
        tpass=request.form['password']
        tpass_md5=to_md5(tpass)
        result=User.query.filter_by(username=tuser).first()       
        if result:
            flash(result.username)  
            if result.password_md5==tpass_md5:
                user_t=result
                login_user(user_t)
                flash(u'成功登录')
                return redirect(url_for('words'))
        flash(u'账号或密码错误，请重新登录~')
    return redirect(url_for('login'))       

@app.route('/logout')  # 登出
def logout():
    logout_user()  # 登出，会话产生的任何cookie都会被清理干净
    flash(u'你已退出系统~')
    return redirect(url_for('home'))




