#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class CommentPostForm(forms.Form):
	'''
	'''
	reply   = forms.CharField(required=True)
	parent  = forms.CharField(required=False)
	
	content = forms.CharField(required=True)
	
