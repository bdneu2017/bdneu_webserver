#coding: utf-8
#encoding:utf-8

from django.db import models
from django.contrib.auth.models import User
#from django.contrib import User
# Create your models here.

class Message(models.Model):
    name = models.CharField(u'发表人名称',max_length=30,default='anonymous')
    title = models.CharField(u'标题',max_length=256)
    content = models.TextField(u'内容')
    email = models.CharField(u'邮箱',max_length=25)
    pub_date = models.DateTimeField(u'发布日期', auto_now_add=True, editable = True)
    class Meta: 
        ordering =['-pub_date']
        
    def __str__(self):
        return self.title


class ScrapyModel(models.Model):
    title=models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    desc = models.TextField()
    def __str__(self):
        return self.title
'''
class My_User(models.Model):
    user=models.OneToOneField(User)
    
    def __str__(self):
        return self.username'''