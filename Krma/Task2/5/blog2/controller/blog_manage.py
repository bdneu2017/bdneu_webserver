# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask_login import login_required, login_user, logout_user, current_user
from blog2.model.User import  User
from blog2.model.Category import Category
from blog2.model.SpiderP9 import SpiderP9
import os

from blog2 import app,db
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g

from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
import flask_admin as admin
from blog_admin import RegistrationForm

import spider as spiderfun


@app.route('/')
def index():
    spider = SpiderP9.query.all()
    return render_template('index.html',entries=spider)


@app.route('/entries/')
#@login_required
def show_entries():
    categorys = Category.query.all()
    return render_template('show_entries.html',entries=categorys)

@app.route('/spider/')
#@login_required
def spider():
    url = "http://psnine.com/"
    msg = SpiderP9.query.all()  
    for u in msg:  
        db.session.delete(u)  
    soup=spiderfun.getsoup(url)
    #qiubai(soup)
    spiderfun.p9(soup)
    return redirect(url_for('index'))

@app.route('/add/',methods=['POST'])
@login_required
def add_entry():
    '''
    if not session.get('logged_in'):
        abort(401)
    '''
    title = request.form['title']
    content = request.form['text']
    userid=current_user.id
    username=current_user.login
    category = Category(title,content,userid,username)
    db.session.add(category)
    try: 
        db.session.commit()
    except:
        flash('标题与已有条目重复，留言失败。')
    else:
        flash('留言成功。')
    return redirect(url_for('show_entries'))

#@app.route('/login',methods=['GET','POST'])
@app.route('/login/',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=request.form['login']).first()

        '''
        passwd = User.query.filter_by(password=request.form['password']).first()

        if user is None:
            error = 'Invalid login'
        elif passwd is None:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        '''

        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('show_entries'))
        else:
            flash('登陆失败，请检查用户名与密码是否正确。')
    return render_template('login.html', error=error)

'''
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=request.form['login']).first()

        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('show_entries'))
        else:
            flash('登陆失败，请检查用户名与密码是否正确。')
    return render_template('login.html', error=error)
'''
#@app.route('/register',methods=['GET','POST'])
@app.route('/register/',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        form = RegistrationForm(request.form)
        user=User()
        form.populate_obj(user)
        user.login = request.form['username']
        user.password = generate_password_hash(form.password.data)
        #user.password = generate_password_hash(request.form['password'])
        user.admin=False
        #login = request.form['username']
        
        #user = User.query.filter_by(username=request.form['username']).first()
        
        #user = User(login, password, admin)
        db.session.add(user)
        try: 
            db.session.commit()
        except:
            flash(len(categorys))
        else:
            flash('注册成功。')
            return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)

'''
@app.route('/register',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = generate_password_hash(request.form['password'])
        admin=False
        user = User(login, password, admin)
        db.session.add(user)
        try: 
            db.session.commit()
        except:
            flash('用户名已被占用，注册失败。')
        else:
            flash('注册成功。')
        return redirect(url_for('show_entries'))
    return render_template('register.html', error=error)
'''
'''
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)
            user.admin=False

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()
'''
@app.route('/logout/')
@login_required
def logout():
    #session.pop('logged_in', None)
    logout_user()
    flash('登出成功。')
    return redirect(url_for('show_entries'))