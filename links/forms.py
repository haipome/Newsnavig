#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class LinkPostForm(forms.Form):
	'''
	'''
	title  = forms.CharField(required=True)
	url    = forms.CharField(required=True)
	topics = forms.CharField(required=False)
	
