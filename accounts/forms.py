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
	                             attrs=dict(maxlength=75)))
	
	password = forms.CharField(label="你的登录密码",
	           widget=forms.PasswordInput())
	
	new_email = forms.EmailField(widget=forms.TextInput(
	                             attrs=dict(maxlength=75)))

class UserLoginForm(forms.Form):
	'''
	'''
	name_or_email = forms.CharField(required=True)
	password = forms.CharField(required=True)
	remember_me = forms.BooleanField(required=False)
	way = forms.CharField(required=False)
	next = forms.CharField(required=False)

class RegistForm(forms.Form):
	'''
	'''
	username = forms.RegexField(regex=USERNAME_RE,
	                            max_length=30,
	                            widget=forms.TextInput())
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)))
	password1 = forms.CharField(widget=forms.PasswordInput(render_value=False))
	password2 = forms.CharField(widget=forms.PasswordInput(render_value=False))
	agreement = forms.BooleanField(required=False)
	
class ResendActiveEmail(forms.Form):
	'''
	'''
	email = forms.EmailField()
	
