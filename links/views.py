#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import LinkPostForm
from links.utils import post_link
from links.models import Link
from django.contrib import messages
from nng.settings import *
from django.core.urlresolvers import reverse

def topics_get(topic_names):
	topics = []
	for n in topic_names:
		if n and len(n) < NAME_MAX_LEN:
			if '/' not in n:
				topics.append(n)
				if len(topics) == MAX_TOPICS_NUMBER:
					return topics
	
	return topics


@login_required
def post(request):
	'''
	'''
	form = LinkPostForm()
	user = request.user
	
	if request.method == 'POST':
		form = LinkPostForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			title, url, topics_n = (data['title'], data['url'],
			     data['topics'].split(' '))
			
			topics = topics_get(topics_n)
			
			if user.user_links.filter(url=url).count():
				messages.error(request, u'你似乎已经发布过这个链接了')
			else:
				if post_link(user, url, title, topics):
					messages.success(request, u'发布成功')
				else:
					messages.error(request, u'发布失败')
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		pass
	
	return HttpResponseRedirect(reverse('homepage'))
	
