#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.timezone import now
from nng.settings import *
from avatars.models import Avatar, get_tag_avatar


class TopicEditForm(forms.Form):
	'''
	'''
	avatar = forms.ImageField(required=False)
	detail = forms.CharField(required=False)
	
	def save(self, t):
		data = self.cleaned_data
		t.detail = data['detail']
		
		if data['avatar']:
			img = data['avatar']
			anonymous = get_tag_avatar()
			if t.avatar == anonymous:
				avatar = Avatar()
				avatar.avatar_save(img)
				t.avatar = avatar
			else:
				t.avatar.avatar_delete()
				t.avatar.avatar_save(img)
		
		try:
			t.save()
		except:
			pass
		
		return t

class TopicsEditForm(forms.Form):
	'''
	'''
	c = forms.CharField(required=True)
	topics = forms.CharField(required=False)
	
