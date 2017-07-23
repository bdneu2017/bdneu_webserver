#coding: utf-8
#encoding: utf-8

from django.shortcuts import render
from .function.getSysInfo import getSysInfo
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .function.forms import AddForm,AddForm2,my_user
from django.core.mail import send_mail
from .models import Message
from django.contrib.auth.models import User
import re
import json

#from nt import strerror
from django.contrib.auth import authenticate, login

#xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
# Create your views here.
items_per_page=6
total_pages=0


def index(request):
    return render(request,'sysinfo/home.html')


def get_info(request):
    info=getSysInfo()
    return render(request,'sysinfo/info.html',
                  {'info':info,})
    
def messageboard(request):
    try:
        posts=Message.objects.all()
    except Exception as e:
        print(e)
    total_pages=items_per_page//items_per_page + 1
    
    return render(request,'sysinfo/messageboard.html',{'posts':posts,
                                                       'total_pages':total_pages,
                                                       'items_per_page':items_per_page})


def accounts(request):
    return render(request,'sysinfo/accounts.html')

def check_user(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        posts=Message.objects.all()
        email=User.objects.get(username=username).email
        #return render(request,'sysinfo/success_login.html',{'username':username,'email':email})
        return render(request,'sysinfo/messageboard2.html',{'username':username,'email':email,"posts":posts})
    else:
        return render(request,'sysinfo/fail_login.html')
    
def login(request):
    posts=Message.objects.all()
    return render(request,'sysinfo/messageboard.html',{'posts':posts})
    
def register(request):
    return render(request,'sysinfo/registration.html')

def regist(request):
    if request.method=='POST':
        user1=my_user(request.POST)
        posts=Message.objects.all()
        if user1.is_valid():
            username1=user1.cleaned_data['username']
            password1=user1.cleaned_data['password']
            email1=user1.cleaned_data['email']
            try:
                user=User.objects.create_user(username1,email1,password1)
                user.save()
            except Exception as e:
                #if re.findall('^IntegrityError',str(e)):
                    #return HttpResponse(u"用户名重复")
                #else:
                    return render(request,'sysinfo/reg_fail.html')
            #return render(request,'sysinfo/reg_success.html',{"username":username1})
            return render(request,'sysinfo/messageboard2.html',{"username":username1,
                                                                "email":email1,
                                                                "posts":posts})
    else:
        #User=User()
        pass
    return HttpResponseRedirect("/registration/")

def test(request):
    return render(request,'sysinfo/test.html')

def forms2db(request):
    if request.method=='POST':
        form=AddForm2(request.POST)
        
        if form.is_valid():
            name=form.cleaned_data['name']
            title=form.cleaned_data['title']
            email=form.cleaned_data['email']
            content=form.cleaned_data['content']
            Message.objects.create(name=name,title=title,content=content,email=email)
            return HttpResponseRedirect('/messageboard/')
            
    else:
        form=AddForm2()
    return HttpResponse("post failed")
    
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))

def djForm(request):
    if request.method=='POST':
        form=AddForm(request.POST)
        
        if form.is_valid():
            a=form.cleaned_data['a']
            b=form.cleaned_data['b']
            return HttpResponse(str(int(a)+int(b)))
    else:
        form=AddForm()
    return render(request,'sysinfo/djForm.html',{'form':form})

def djAjax_index(request):
    return render(request,'sysinfo/djAjax1.html')

def djAjax_index2(request):
    return render(request,'sysinfo/djAjax2.html')


def ajax_list(request):
    a = list(range(100))
    return HttpResponse(json.dumps(a), content_type='application/json')

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

def email(request):
    return render(request,'sysinfo/email.html')            
            
def base(request):
    return render(request,'sysinfo/base.html')
