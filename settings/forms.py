#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from nng.settings import *
from avatars.models import Avatar

class NameChangeForm(forms.Form):
	'''
	'''
	new_name = forms.CharField(widget=forms.TextInput(
	                           attrs=dict(maxlength=30)),
	                           label=u"你想更改的名字")
	
class DetailChangeForm(forms.Form):
	'''
	'''
	website = forms.URLField(required=False, max_length=200, 
	                         label=u"个人网站")
	
	signature = forms.CharField(required=False, widget=forms.TextInput(
	                           attrs=dict(maxlength=210)),
	                           label=u"一句话签名")
	
	detail = forms.CharField(required=False, widget=forms.Textarea(
	                          attrs=dict(maxlength=3000)),
	                          label=u"个人说明")
	
	def save(self, profile, data):
		profile.website = data['website']
		profile.signature = data['signature']
		profile.detail = data['detail']
		profile.save()

class AvatarChangeForm(forms.Form):
	'''
	'''
	img = forms.ImageField()
	
	def save(self, user, request):
		img = request.FILES.get('img', None)
		if img:
			anonymous = User.objects.get(pk=ANONYMOUS_ID)
			if user.userprofile.avatar != anonymous.userprofile.avatar:
				user.userprofile.avatar.avatar_delete()
				user.userprofile.avatar.avatar_save(img)
			else:
				avatar = Avatar()
				avatar.avatar_save(img)
				user.userprofile.avatar = avatar

