#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from avatars.models import Avatar
from django.contrib.auth.models import User
from nng.settings import *
from accounts.models import UserAccount

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

USERNAME_RE = r'^[a-z][a-z0-9]+$'
class RegistForm(forms.Form):
	'''
	'''
	username = forms.RegexField(regex=USERNAME_RE,
	                            max_length=30,
	                            widget=forms.TextInput(),
	                            label= u'用户名',
	                            error_messages=
	           {'invalid': u'不合法的用户名：只允许小写字母和数字，并且开头不能为数字'})
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)),
	                         label=u'电子邮箱地址')
	password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
	                             label="密码")
	password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
	                            label=u"重复密码")
	
