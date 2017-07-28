# coding:utf-8
from app import app
from flask import render_template, flash, request, redirect
from flask_login import LoginManager, login_user, logout_user
from users_class import User
from werkzeug.security import check_password_hash


login_manager = LoginManager(app)
login_manager.session_protection = 'strong'  # cookie篡改时session被删除
login_manager.login_view = '/'  # 未登录时访问需要登录的页面 重定向到主页
login_manager.login_message = u'请登录后访问'  # 自定义flash消息
login_manager.login_message_category = 'info'  # flash消息的级别


@app.route('/login', methods=['GET'])  # 登录页面
def login():
    return render_template('login.html')


@app.route('/verify', methods=['POST'])  # 验证 登入
def verify():  # 验证
    tuser = request.form['username']
    tpass = request.form['password']
    result = User.query.filter_by(username=tuser).first()
    if result:
        if check_password_hash(result.password_hash, tpass):
            user_t = result
            login_user(user_t)
            flash(user_t.username + u'成功登录')
            return redirect('words')
    flash(u'账号或密码错误，请重新登录~')
    return redirect('login')


@app.route('/logout')  # 登出
def logout():
    logout_user()  # 登出，会话产生的任何cookie都会被清理干净
    flash(u'你已退出系统~')  # 退出 回到主页
    return redirect('')  # url_for 函数名 redirect 地址
