#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class DiscussPostForm(forms.Form):
	'''
	'''
	title  = forms.CharField(required=True)
	detail = forms.CharField(required=False)
	topics = forms.CharField(required=False)
