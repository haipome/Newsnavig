#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class DiscussPostForm(forms.Form):
	'''
	'''
	goback = forms.CharField(required=False)
	
	title  = forms.CharField(required=True)
	detail = forms.CharField(required=False)
	topics = forms.CharField(required=False)

class DiscussEditForm(forms.Form):
	'''
	'''
	discuss_id = forms.CharField(required=True)
	title  = forms.CharField(required=True)
	detail = forms.CharField(required=False)
	topics = forms.CharField(required=False)
