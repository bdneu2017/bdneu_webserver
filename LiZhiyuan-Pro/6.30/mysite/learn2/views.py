#coding:utf-8
from django.shortcuts import render
from .function.getSysInfo import getSysInfo
import time

# Create your views here.

def home(request):
    #string = u"气沉丹田"
    #List = map(str, range(100))# 一个长度为100的 List
    #List2=['1','','2','3']
    #List2=[]
    info=getSysInfo()
    time_t=time.asctime()
    time_t=u'当前服务器时间：'+time_t
    return render(request,'learn2/home.html',{
                                              'info':info,
                                              't_now':time_t
                                              })