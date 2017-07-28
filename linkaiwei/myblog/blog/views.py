# -*-coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django import forms

from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment
from .forms import CommentForm,UserForm,LoginForm,ChangepwdForm

import urllib,urllib2,re

def login_validate(request,username,password):
    rtvalue = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            auth_login(request,user)
            return True
    return rtvalue

def mylogin(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if login_validate(request,username,password):
                request.session['username']=username
                return render(request,'success.html',{'user':username})
            else:
                error.append('Please input the correct password')
        else:
            error.append('Please input both username and password')
    else:
        form = LoginForm()
    return render(request,'login.html',{'error':error,'form':form})

@login_required
def mylogout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def changepassword(request,username):
    error = []
    if request.method == 'POST':
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=username,password=data['old_pwd'])
            if user is not None:
                if data['new_pwd']==data['new_pwd2']:
                    newuser = User.objects.get(username__exact=username)
                    newuser.set_password(data['new_pwd'])
                    newuser.save()
                    return HttpResponseRedirect('/login/')
                else:
                    error.append('Please input the same password')
            else:
                error.append('Please correct the old password')
        else:
            error.append('Please input the required domain')
    else:
        form = ChangepwdForm()
    return render(request,'changepassword.html',{'form':form,'error':error})

def register(request):
    error=[];
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2=uf.cleaned_data['password2']
            email = uf.cleaned_data['email']
            if not User.objects.all().filter(username=username):
                if uf.pwd_validate(password, password2):
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    login_validate(request, username, password)
                    return render(request,'success.html', {'user': username})
                else:
                    error.append('Please input the same password')
            else:
                error.append('The username has existed,please change your username')
    else:
        uf = UserForm()
    return render(request,'register.html',{'uf':uf})


def get_blogs(request,username=0):
    ctx = {
        'blogs': Blog.objects.all().order_by('-created')
    }
    return render(request, 'blog-list.html', ctx,{'username':username})


def get_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)

    ctx = {
        'blog': blog,
        'comments': blog.comment_set.all().order_by('-created'),
        'form': form
    }
    return render(request, 'blog-detail.html', ctx)

#从糗事百科抓取文字笑话的函数
def get_jokes(request):
    url = 'http://www.qiushibaike.com/hot/page/'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>', re.S)
        items = re.findall(pattern, content)
        return JsonResponse(items, safe=False)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason