# coding:utf-8
from app import app, db
from users_class import User
from flask import flash, redirect, render_template, request
from database import user_role
import sqlalchemy

# 注册系统


@app.route('/register')
def register():  # 注册页面
    return render_template('register.html')


@app.route('/updates', methods=['POST'])
def update_register():
    username = request.form['username']
    password = request.form['password']  # 密码需要安全性判断
    if username == '':
        flash(u'昵称不能为空~**~')
        return redirect('register')
    if password == '':
        flash(u'密码不能为空~**~')
        return redirect('register')
    user_t = User(username, password, user_role.id)
    try:
        db.session.add(user_t)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flash(u'该昵称已被注册~换一个吧~,~')
        return redirect('register')  # redirect 地址
    return redirect('login')
