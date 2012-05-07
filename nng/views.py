#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from topics.models import TopicUserShip
from nng.settings import LATEST_TOPICS_NUMBER
from dynamic.utils import get_dynamics
from discusses.utils import get_discusses
from explore.views import process_pager
from datetime import date
from dateutil import tz
from nng.settings import TIME_ZONE, MESSAGES_PER_PAGE
from django.contrib.contenttypes.models import ContentType

def get_user_topics(user):
	if user.is_authenticated():
		return user.user_topics.order_by(
		             '-topicusership__last_active_time')[:LATEST_TOPICS_NUMBER]
	else:
		return None


def get_follows(user):
	'''
	'''
	user_type   = ContentType.objects.get(app_label='profiles', model='userprofile')
	topic_type  = ContentType.objects.get(app_label='topics',   model='topic')
	domain_type = ContentType.objects.get(app_label='domains',  model='domain')
	
	columns = user.userdata.follows.all().prefetch_related(
	          'content_object__avatar')
	
	follows = []
	follows_user = []
	follows_topic = []
	follows_domain = []
	
	for c in columns:
		follows.append(c)
		if c.content_type == user_type:
			follows_user.append(c.content_object)
		elif c.content_type == topic_type:
			follows_topic.append(c.content_object)
		elif c.content_type == domain_type:
			follows_domain.append(c.content_object)
		else:
			pass
	
	user_self = user.userprofile.get_column()
	if user_self not in follows:
		follows.append(user.userprofile.get_column())
	
	return (follows, follows_user, follows_topic, follows_domain, user_self)


def index(request):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	user = request.user
	if not user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	
	user_topics = get_user_topics(user)
	
	follow = get_follows(user)
	dynamics = get_dynamics(follow[0], s, e)
	
	today = date.today()
	local = tz.gettz(TIME_ZONE)
	
	for d in dynamics:
		d.time = d.time.astimezone(local)
	
	if len(dynamics) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('dynamic.html', 
	                         {'user_topics': user_topics,
	                          'follow': follow,
	                          'dynamics':dynamics,
	                          'today': today,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))
	


def discuss(request, t='follow'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	user = request.user
	if not user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	
	user_topics = get_user_topics(user)
	follow = get_follows(user)
	
	if t == 'follow':
		discusses = get_discusses(follow[0], s, e)
	elif t == 'reply':
		discusses = user.userdata.discusses.order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'user__userprofile__avatar',
		            'last_active_user__userprofile',)
	elif t == 'me':
		discusses = user.user_discusses.order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'user__userprofile__avatar',
		            'last_active_user__userprofile',)
	else:
		raise Http404
	
	today = date.today()
	local = tz.gettz(TIME_ZONE)
	for d in discusses:
		if d.last_active_time:
			d.last_active_time = d.last_active_time.astimezone(local)
	
	if len(discusses) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('discuss.html', 
	                         {'user_topics': user_topics,
	                          'follow': follow,
	                          'discusses':discusses,
	                          'today': today,
	                          't': t,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))



@login_required
def post(request):
	'''
	'''
	user = request.user
	
	user_topics = get_user_topics(user)
	
	return render_to_response('post.html',
	                         {'user_topics': user_topics,},
	                           context_instance=RequestContext(request))
	
