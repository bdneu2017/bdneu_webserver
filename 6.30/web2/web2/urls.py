# -*- coding: utf-8 -*-
"""web2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webapp1 import views
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout




urlpatterns = [
    url(r'^admin/', admin.site.urls),  # 管理员页面
    url(r'^main/', views.main),  # 主页面
    url(r'^register/', views.register),  # 注册
    url(r'^register/success/', views.register_success),  # 注册成功页面
    url(r'^accounts/login/', views.login, ),  # 登陆页面
    url(r'^logout/', views.logout),  # 注销页面
    url(r'^accounts/auth/', views.auth_view),  # 认证 页面
    url(r'^accounts/loggedin/', views.loggedin),  # 登陆成功页面
    url(r'^accounts/invalid/', views.invalid_login),  # 登陆失败页面
    url(r'^post/', views.msg_post_page),  # 将留言板显示到主页
    url(r'^accounts/change', views.change),  # 修改密码页面
    url(r'^url/', views.url)
]