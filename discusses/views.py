#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import DiscussPostForm
from discusses.utils import post_discuss
from django.contrib import messages
from nng.settings import *
from django.core.urlresolvers import reverse
from links.views import topics_get

@login_required
def post(request):
	'''
	'''
	form = DiscussPostForm()
	user = request.user
	
	if request.method == 'POST':
		form = DiscussPostForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			title, detail, topics_n = (data['title'], data['detail'],
			        data['topics'].split(' ')[:MAX_TOPICS_NUMBER])
			
			topics = topics_get(topics_n)
			
			if post_discuss(user, title, detail, topics):
				messages.success(request, u'发布成功')
			else:
				messages.error(request, u'发布失败')
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		pass
	
	return HttpResponseRedirect(reverse('homepage'))
	
