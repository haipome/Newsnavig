#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from avatars.models import Avatar
from django.contrib.auth.models import User
from nng.settings import *

class EmailChangeForm(forms.Form):
	'''
	'''
	old_email = forms.EmailField(widget=forms.TextInput(
	                             attrs=dict(maxlength=75)),
	                             label=u"你现在使用的邮箱地址")
	
	password = forms.CharField(label="你的登录密码",
	           widget=forms.PasswordInput())
	
	new_email = forms.EmailField(widget=forms.TextInput(
	                             attrs=dict(maxlength=75)),
	                             label=u"你想设置的新的邮箱地址")

class UserLoginForm(forms.Form):
	'''
	'''
	name_or_email = forms.CharField(widget=forms.TextInput(
	                                attrs=dict(maxlength=30)),
	                                label=u"邮箱或用户名")
	
	password = forms.CharField(label="你的登录密码",
	                           widget=forms.PasswordInput())
	
	remember_me = forms.BooleanField(widget=forms.CheckboxInput(),
                                     required=False,
                  label=u'在这台电脑上记住我')
	
