# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from blog2.controller import blog_manage, blog_admin
from blog2.model import User,Category
#from blog2 import models,views

#引用包
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user
from blog2.model.User import  User
from blog2.model.Category import Category
from blog2.model.SpiderP9 import SpiderP9
from blog2.model.Keywords import Keywords
import os

from blog2 import app,db
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g

from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash
import flask_admin as admin


import spider as spiderfun
import keywords

def findSubstrings(substrings,destString):
    res =  map(lambda x:str([destString.index(x),x]),filter(lambda x:x in destString,substrings))
    if res:
        return ', '.join(list(res))

def keynum(content,s2):
    num=map(lambda x:content.count(x),s2)
    dict=zip(s2,num)
    return dict

s1 = '123456789123456'
s2=['123456']
user_input=raw_input('Leave your comments:  ')
print keynum(user_input,s2)
print findSubstrings(s2,user_input)
print type(Keywords.query.all())
