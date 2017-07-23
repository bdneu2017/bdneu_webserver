# encoding: utf-8
#-*-coding:utf-8-*-
'''
Created on

@author: David
'''
from django import forms

class AddForm(forms.Form):
    a=forms.IntegerField()
    b=forms.IntegerField()

class AddForm2(forms.Form):
    name=forms.CharField()
    title=forms.CharField()
    email=forms.CharField()
    content=forms.CharField()

class my_user(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    email=forms.CharField()