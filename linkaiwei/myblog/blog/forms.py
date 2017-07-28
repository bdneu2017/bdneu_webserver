# -*-coding:utf-8 -*-
#
# Copyright (C) 2015-2018 Engine Studio All rights reserved.
# Created on 2016-04-01, by Danny
#

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密 码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput)
    email = forms.EmailField(label='e-mail')
    def pwd_validate(self, p1, p2):
        return p1 == p2

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ChangepwdForm(forms.Form):
    old_pwd=forms.CharField(widget=forms.PasswordInput)
    new_pwd = forms.CharField(widget=forms.PasswordInput)
    new_pwd2 = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):#评论表单

    name = forms.CharField(label='称呼', max_length=16, error_messages={
        'required': '请填写您的称呼',
        'max_length': '称呼太长'
    })

    email = forms.EmailField(label='邮箱', error_messages={
        'required': '请填写您的邮箱',
        'invalid': '邮箱格式不正确'
    })

    content = forms.CharField(label='评论内容', error_messages={
        'required': '请填写您的评论内容',
        'max_length': '评论内容太长'
    })
