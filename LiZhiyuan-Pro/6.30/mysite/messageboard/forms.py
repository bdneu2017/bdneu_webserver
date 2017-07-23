# encoding: utf-8
#-*-coding:utf-8-*-
'''
Created on 2017/6/29

@author: David
'''

from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    email = forms.EmailField(label='电子邮箱', required=False)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(u'^[\u4e00-\u9fa5 _ a-zA-Z0-9]+$', username):
            raise forms.ValidationError(username)
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('此用户名已存在！')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('此电子邮箱已存在！')
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('两次输入的密码不相同！')