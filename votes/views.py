#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
from votes.utils import vote_obj
from shares.utils import post_share
from collect.utils import collect
from string import atoi

def operate(request):
	'''
	'''
	user = request.user
	if not user.is_authenticated():
		return HttpResponse('needlogin')
	c = None
	if request.method == 'GET':
		if 'c' in request.GET and request.GET['c']:
			c = request.GET['c']
		if c:
			items = c.split('-')
			a = items[0]
			t = items[1]
			i = atoi(items[2])
			if a:
				if a == 'v':
					operater = vote_obj
				elif a == 's':
					operater = post_share
				elif a == 'c':
					operater = collect
				else:
					raise Http404
			
			if t == 'l' and i:
				try:
					obj = Link.objects.get(id__exact=i)
				except:
					raise Http404
			elif t == 'd' and i:
				try:
					obj = Discuss.objects.get(id__exact=i)
				except:
					raise Http404
			elif t == 'c' and i:
				try:
					obj = Comment.objects.get(id__exact=i)
				except:
					raise Http404
			else:
				raise Http404
			
			if obj:
				if operater(user, obj):
					return HttpResponse('success')
	
	return HttpResponse('False')
		
