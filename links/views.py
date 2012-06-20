#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import LinkPostForm
from links.utils import post_link
from links.models import Link
from django.contrib import messages
from nng.settings import *
from django.core.urlresolvers import reverse
from string import atoi
from comments.utils import comment_sort
from comments.models import Comment

def topics_get(topic_names):
	topics = []
	for n in topic_names:
		if n:
			n = n[:NAME_MAX_LEN]
			if '/' not in n and n not in topics:
				topics.append(n)
				if len(topics) == MAX_TOPICS_NUMBER:
					return topics
	
	return topics[::-1]


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
			
			title = title[:TITLE_MAX_LEN]
			topics = topics_get(topics_n)
			
			links = user.user_links.filter(
			        url__iexact=url).filter(
			        is_visible=True).all()
			if links:
				l = links[0]
				messages.error(request, u'你已发布过该网址')
				return HttpResponseRedirect(reverse('show_link', args=[l.id]))
			else:
				l = post_link(user, url, title, topics)
				
				if not l:
					messages.error(request, u'发布失败')
			
			if data['goback'] or not l:
				try:
					from_url = request.META['HTTP_REFERER']
					return HttpResponseRedirect(from_url)
				except KeyError:
					pass
			
			return HttpResponseRedirect(reverse('show_link', args=[l.id]))
	
	return HttpResponseRedirect(reverse('homepage'))


def show_link(request, link_id):
	'''
	'''
	link = get_object_or_404(Link, id=atoi(link_id))
	if link.is_visible == False:
		raise Http404
	
	comments = link.comments.filter(
	           is_visible=True).all(
	           ).prefetch_related(
	           'user__userprofile__avatar')
	
	comments = comment_sort(comments, COMMENT_DEEPS)
	
	return render_to_response('link/show_link.html',
	                         {'link': link,
	                          'comments': comments,},
	                         context_instance=RequestContext(request))
	
