#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from nng.settings import *
from avatars.models import Avatar


class ProfileForm(forms.Form):
	'''
	'''
	name = forms.CharField(required=False)
	avatar = forms.ImageField(required=False)
	website = forms.CharField(required=False)
	signature = forms.CharField(required=False)
	detail = forms.CharField(required=False)
	
	def save(self, profile, data):
		if profile.name != data['name']:
			profile.change_name(data['name'][:NAME_MAX_LEN])
		
		profile.website = data['website']
		profile.signature = data['signature'][:SIGNATURE_MAX_LEN]
		profile.detail = data['detail']
		
		if data['avatar']:
			img = data['avatar']
			anonymous = User.objects.get(pk=ANONYMOUS_ID)
			if profile.avatar != anonymous.userprofile.avatar:
				profile.avatar.avatar_delete()
				profile.avatar.avatar_save(img)
			else:
				avatar = Avatar()
				avatar.avatar_save(img)
				profile.avatar = avatar
		try:
			profile.save()
		except:
			pass
		return profile
	
