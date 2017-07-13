# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from webapp1.models import *
from forms import MsgPostForm
from django.views.generic import ListView
from django.contrib.auth.models import User
from forms import UserForm
from forms import ChangepwdForm
from forms import UrlForm
from models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.middleware import csrf
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
import urllib2
items_per_page=10


def msg_list_page(request):  #实现分页功能
    return ListView.object_list(request,
                                   queryset=MsgPost.objects.order_by('-id'),
                                   paginate_by=items_per_page,
                                   page=1,
                                   template_name='main.html',
                                   template_object_name='main.html'
                                   )


def main(request):#显示主页
    posts = MsgPost.objects.all()
    return render_to_response('main.html', locals())


'''def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user( username=form.cleaned_data['username'],
                                             email=form.cleaned_data['email'],
                                             password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/main/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request,{'form':form})
    return render_to_response('register.html',variables)'''


def login(request):  # 登陆页面
    c = {}
    c.update(request)
    return render_to_response('login.html', c)


def auth_view(request):  # 认证用户登录
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print (username)
    print (password)
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return render(request, 'loggedin.html', {'data': username+"登陆成功"})
    else:
        return render(request, 'invalid.html', {'data': "账号或密码错误！"})


'''def login(req):
    if req.method == 'POST':
        uf = UserLog(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username=username, password=password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/accounts/loggedin/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/accounts/invalid/')
    else:
        uf = UserForm()
    return render(req, 'loggedin.html', {'uf': uf})

'''


def loggedin(request):  # 用户已登陆页面
    return render_to_response('loggedin.html',  {'full_name': request.user.username})


def invalid_login(request): # 登陆失败页面
    return render_to_response('invalid_login.html')


def logout(request):  # 注销处理
    auth.logout(request)
    return render_to_response('logout.html')


def register(request):  # 实现注册功能
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password1 = uf.cleaned_data['password1']
            password2 = uf.cleaned_data['password2']
            email = uf.cleaned_data['email']
            user = User.objects.filter(username=username)
            if user.exists():

                return render_to_response('register_fail.html', {'data': "用户名已被占用！请更换"})
            if password1 != password2:

                return render_to_response('register_fail.html', {'data': "前后密码不一致"})
            #将表单写入数据库
            user = User.objects.create_user(username=username,email=email,password=password2)
            '''user.username = username
            user.password = password2
            user.email = email'''
            user.save()
            #返回注册成功页面
            return render(request, 'register_success.html', {'username':username})
    else:
        uf = UserForm()
    return render(request, 'register.html', {'uf': uf})


def register_success(request):
    return render_to_response('register_success.html')


@login_required  # 装饰器，检查是否在登录状态，不在登录状态自动返回login页面
def msg_post_page(request):  # 实现留言功能
    if request.method == 'POST':
        form = MsgPostForm(request.POST)
        if form.is_valid():
            '''newmessage = MsgPost(title=form.cleaned_data['title'],content=form.cleaned_data['content'],# user=request.user )
            newmessage.save()'''
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            message = MsgPost()
            message.title = title
            message.content = content
            message.user = request.user.username
            message.datetime = datetime
            message.save()
        return HttpResponseRedirect('/main/')
    else:
        form = MsgPostForm()
    # variables = RequestContext(request, {'form': form})
    return render_to_response('msg_post_page.html', {'form': form})


@login_required
def change(request):  # 实现修改密码功能
    if request.method == "POST":
        ch = ChangepwdForm(request.POST)
        if ch.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                return render(request, 'change_success.html', {'username': username})
            else:
                return render(request, 'change_fail.html', {'username': username})
        return render(request, 'change_fail.html')
    else:
        ch = ChangepwdForm(request.POST)
        return render(request, 'change.html', {'ch': ch})


@login_required
def url(request):  # 实现爬取网页
    if request.method == "POST":
        url1 = request.POST.get('url', '')
        response = urllib2.urlopen(url1)
        content = response.read()
        print response.read()
        return render(request, 'url.html', {'data': content})
    else:
        return render(request, 'url.html')
