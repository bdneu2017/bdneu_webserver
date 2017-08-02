# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from blog2 import app, db
from flask import Flask, url_for, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

from blog2.model.User import  User
from blog2.model.Category import Category
from blog2.model.SpiderP9 import SpiderP9
from blog2.model.Keywords import Keywords
from keywords import keynum2
'''
# Create Flask application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

'''

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('用户不存在。')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('密码错误。')
        '''
        if user.admin is False:
            raise validators.ValidationError('用户无后台管理权限。')
        '''
    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('用户名已被占用。')


# Initialize flask-login
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if hasattr(login.current_user, 'admin'):
            if login.current_user.admin is True:
                return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        #link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        #self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()
    '''
    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)
            user.admin = True

            db.session.add(user)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()
    '''
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

class KeyAddView(admin.BaseView):
    
    @expose('/')
    def keyadd(self):
        return self.render('keyadd.html')

    @expose('/add_key/',methods=['POST'])
    def add_key(self):
        '''
        if not session.get('logged_in'):
            abort(401)
        '''
        keyword=Keywords()
        keyword.key = request.form['key']
        #print type(request.form['warning'])
        #print request.form['warning']
        keyword.warning = request.form.has_key('warning')
        #print request.form.has_key('warning')
        db.session.add(keyword)
        try: 
            db.session.commit()
        except:
            flash('标题与已有条目重复，留言失败。')
        else:
            flash('关键字添加成功。')
            key=Keywords.query.all()
            #keynum2(category,key)
            db.session.commit()
            keyend=Keywords.query.order_by(desc(Keywords.id)).first()
            categorys = Category.query.all()
            if keyend.times is 0:
                for content in categorys:
                    keyend=keynum2(content,keyend)
                db.session.commit()
        return redirect(url_for('.keyadd'))

class KeywordsView(MyModelView):
    #can_create = False
    create_template = 'keyadd.html'
    #name=u'关键字'
    column_labels=dict(key=u'关键字',times=u'出现次数',warning=u'高危（出现即报警）')
    #form_columns = ['Key', 'Times','Warning']

# Flask views
'''
class MyView(admin.BaseView):

    @expose('/rules/')
    def rules(self):

        return self.render('index.html')
'''
'''
class RulesView(admin.BaseView):
    def is_accessible(self):
        if hasattr(login.current_user, 'admin'):
            if login.current_user.admin is True:
                return login.current_user.is_authenticated
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
        
#这里类似于app.route()，处理url请求
    @expose('/')
    def index(self):
        
        return self.render('admin/rules.html')
'''



class MyAdminView(admin.BaseView):
    @admin.expose('/')
    def index(self):
        return self.render('myadmin.html')

# Initialize flask-login
init_login()

# Create admin
admin = admin.Admin(app, '留言板后台', index_view=MyAdminIndexView(), base_template='my_master.html')

admin.add_view(MyModelView(User, db.session,name='用户'))
admin.add_view(MyModelView(Category, db.session,name='留言'))
admin.add_view(MyModelView(SpiderP9, db.session,name='爬虫'))

admin.add_view(KeyAddView(name='添加',endpoint='keyadd', category='关键字'))
admin.add_view(KeywordsView(Keywords, db.session,name='管理',endpoint='keymanage',category='关键字'))
#admin.add_view(RulesView(url='rules/',name='规则'))
#admin.add_view(MyAdminView(name="view1", category='Test'))

from flask_admin.contrib.fileadmin import FileAdmin

import os.path as op


basedir = os.path.abspath(os.path.dirname(__file__))
file_path = op.join(basedir, 'static')
admin.add_view(FileAdmin(app.config['FILEDIR'], '/upload', name='文件'))

#form_extra_fields = {'pics': upload.ImageUploadField(label=u'图片',base_path=file_path)}