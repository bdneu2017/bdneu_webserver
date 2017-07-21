# coding:utf-8
from app import app,db
from classes import User
from flask import flash,redirect,render_template,request
from md5 import to_md5
from database import user_role
#注册系统


@app.route('/register')
def register():#注册页面
    return render_template('register.html')

@app.route('/updates',methods=['GET','POST'])
def update_register():
    if request.method=='GET':
        flash(u'请提交注册信息')        
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        password_md5=to_md5(password)
        user_t=User(username,password_md5,user_role.id) 
        '''db.session.add(user_t) 
                                db.session.commit()'''
        try:
            db.session.add(user_t) 
            db.session.commit() 
        except:
            flash(u'该用户名已被注册~请换一个吧')
        return redirect('login')  
    return redirect('register')
