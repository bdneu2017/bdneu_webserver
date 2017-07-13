# -*- coding: utf-8 -*-
from django import forms
import re
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import MsgPost



'''class UserLog(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())'''


class UserForm(forms.Form):   # 用户登陆表单
    username = forms.CharField(label='用户名', max_length=20)
    email = forms.EmailField(label='电子邮箱', required=False)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput())

    '''def cleaned_name(self): # 表单里的过滤函数
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError('用户名已存在！')
        else:
            return username

    def cleaned_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('用户名已存在！')
        else:
            return email'''

    '''def cleaned_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            else:
                raise forms.ValidationError('输入密码不一致！')'''


class MsgPostForm(forms.Form):   #留言表单
    title = forms.CharField(label='标题', max_length=100)
    content = forms.CharField(label='内容', widget=forms.Textarea)

    '''def clean_title(self):
        title = self.cleaned_data['title']
        try:
            MsgPost.objects.filter(title=title)
        except ObjectDoesNotExist:
            return title
        raise forms.ValidationError('此标题已存在！')'''


class ChangepwdForm(forms.Form):      # 修改密码表单
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"原密码",
            }
        ),
    )

    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )

    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
    )

    def clean(self):  # 重写form.clean方法
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] !=self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class UrlForm(forms.Form):
    url = forms.CharField(label='网址', max_length=100)
    content = forms.CharField(label='页面源码', widget=forms.Textarea)