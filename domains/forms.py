#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.timezone import now
from nng.settings import *
from avatars.models import Avatar, get_tag_avatar


class DomainEditForm(forms.Form):
	'''
	'''
	name = forms.CharField(required=False)
	avatar = forms.ImageField(required=False)
	detail = forms.CharField(required=False)
	
	def save(self, d):
		data = self.cleaned_data
		d.name = data['name'][:NAME_MAX_LEN]
		d.detail = data['detail']
		
		if data['avatar']:
			img = data['avatar']
			anonymous = get_tag_avatar()
			if d.avatar == anonymous:
				avatar = Avatar()
				avatar.avatar_save(img)
				d.avatar = avatar
			else:
				d.avatar.avatar_delete()
				d.avatar.avatar_save(img)
		
		try:
			d.save()
		except:
			pass
		
		return d
