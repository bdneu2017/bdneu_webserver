# coding:utf-8
from register import register  # to be used
from admin_manage import admin  # to be used
from login import login_manager
from flask import render_template
from users_class import User
from app import app
import sys

from chat_online import socketio
reload(sys)
sys.setdefaultencoding('utf8')


@login_manager.user_loader
def load_user(userid):
    user = User.query.get(userid)
    return user
# 主页


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
