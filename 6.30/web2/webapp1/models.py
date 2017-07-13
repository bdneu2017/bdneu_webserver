# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MsgPost(models.Model):  # 留言板模型
    user = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']


'''class User(auth_user):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()'''


class UserAdmin(admin.ModelAdmin):   # 管理员页面显示用户
    list_display = ('username', 'email')


'''admin.site.register(User, UserAdmin)'''
