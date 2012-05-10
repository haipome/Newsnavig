#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from topics.models import Topic
from forms import TopicEditForm
from django.http import Http404
from explore.views import process_pager
from nng.settings import MESSAGES_PER_PAGE
from data.models import FollowShip

def topic(request, topic_name, t='links'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request, limit=False)
	
	topic = get_object_or_404(Topic, name__iexact=topic_name)
	column = topic.get_column()
	
	followers_ship = FollowShip.objects.filter(
	                 column=column).all(
	                 )[:MESSAGES_PER_PAGE].prefetch_related(
	                 'userdata__user__userprofile__avatar')
	
	followers = [obj.userdata.user.userprofile for obj in followers_ship]
	
	if t == 'links':
		datas = topic.topic_links.filter(
		        is_visible=True).all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar', 'domain')
	elif t == 'links-super':
		datas = datas = topic.topic_links.filter(
		        is_visible=True).filter(
		        is_boutique=True).all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar', 'domain')
	elif t == 'discusses':
		datas = topic.topic_discusses.filter(
		        is_visible=True).order_by(
		        '-last_active_time').all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar',
		        'last_active_user__userprofile',)
	elif t == 'discusses-super':
		datas = topic.topic_discusses.filter(
		        is_visible=True).filter(
		        is_boutique=True).order_by(
		        '-last_active_time').all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar',
		        'last_active_user__userprofile',)
	elif t == 'followers':
		followers_ship = FollowShip.objects.filter(
		                 column=column).all(
		                 )[s:e].prefetch_related(
		                 'userdata__user__userprofile__avatar')
		
		datas = [(obj.userdata.user.userprofile, \
		          obj.column) for obj in followers_ship]
	else:
		raise Http404
	
	if len(datas) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('topic/topic_home.html',
	                         {'topic': topic,
	                          'column': column,
	                          't': t,
	                          'followers': followers,
	                          'datas': datas,},
	                           context_instance=RequestContext(request))
	
@login_required
def edit(request, topic_name):
	'''
	'''
	if request.method == 'POST':
		form = TopicEditForm(request.POST, request.FILES)
		if form.is_valid():
			topic = get_object_or_404(Topic, name__iexact=topic_name)
			form.save(topic)
			
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		raise Http404
	
