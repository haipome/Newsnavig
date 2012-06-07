#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from topics.models import Topic
from forms import TopicEditForm, TopicsEditForm
from django.http import Http404
from explore.views import process_pager
from nng.settings import MESSAGES_PER_PAGE
from data.models import FollowShip
from links.views import topics_get
from string import atoi
from links.models import Link
from discusses.models import Discuss
from utils import add_link_topic, add_discuss_topic, del_link_topic, del_discuss_topic
from django.utils.encoding import smart_str, smart_unicode
from dynamic.models import Dynamic
from discusses.models import DiscussIndex
from django.utils import timezone
from nng.settings import *

def topic(request, topic_name, t='links'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request, limit=False)
	
	topic = get_object_or_404(Topic, name__iexact=topic_name)
	column = topic.get_column()
	
	followers_ship = FollowShip.objects.filter(
	                 column=column).all(
	                 )[:TAG_FOLLOWS_NUM].select_related(
	                 'userdata__user__userprofile__avatar')
	
	followers = [obj.userdata.user.userprofile for obj in followers_ship]
	
	if t == 'links':
		datas = topic.topic_links.filter(
		        is_visible=True).all(
		        )[s:e].select_related(
		        'user__userprofile__avatar', 'domain')
	elif t == 'links-super':
		datas = datas = topic.topic_links.filter(
		        is_visible=True).filter(
		        is_boutique=True).all(
		        )[s:e].select_related(
		        'user__userprofile__avatar', 'domain')
	elif t == 'discusses':
		datas = topic.topic_discusses.filter(
		        is_visible=True).order_by(
		        '-last_active_time').all(
		        )[s:e].select_related(
		        'user__userprofile__avatar',
		        'last_active_user__userprofile',)
	elif t == 'discusses-super':
		datas = topic.topic_discusses.filter(
		        is_visible=True).filter(
		        is_boutique=True).order_by(
		        '-last_active_time').all(
		        )[s:e].select_related(
		        'user__userprofile__avatar',
		        'last_active_user__userprofile',)
	elif t == 'followers':
		followers_ship = FollowShip.objects.filter(
		                 column=column).all(
		                 )[s:e].select_related(
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

def topics_change(t, i, topics, user):
	'''
	'''
	try:
		topics_name = topics_get(topics.lower().split(' '))
		
		if t == 'l' and i:
			obj = Link.objects.get(pk=i)
		elif t == 'd' and i:
			obj = Discuss.objects.get(pk=i)
		else:
			return False
		
		if obj.user != user:
			return False
		
		is_b = obj.is_boutique
		old_topics = obj.topics.all()
		old_topics_name = []
		for topic in old_topics:
			name = topic.name.lower()
			if name not in topics_name:
				if isinstance(obj, Link):
					del_link_topic(obj, topic)
				elif isinstance(obj, Discuss):
					del_discuss_topic(obj, topic)
				else:
					return False
				obj.topics.remove(topic)
			else:
				old_topics_name.append(name)
		
		for t_name in topics_name:
			if t_name not in old_topics_name:
				if isinstance(obj, Link):
					topic = add_link_topic(t_name, user, obj.url, obj.domain)
					column = topic.get_column()
					if is_b:
						topic.n_links_boutiques += 1
						topic.save()
					if (not FILTER and \
					   topic.topic_links.filter(url__iexact=obj.url
					   ).count() == 0) or \
					   (FILTER and is_b):
						Dynamic.objects.create(column=column,
						                       way=WAY_LINK_TOPIC_POST,
						                       content_object=obj)
				elif isinstance(obj, Discuss):
					topic = add_discuss_topic(t_name, user)
					column = topic.get_column()
					if is_b:
						topic.n_discusses_boutiques += 1
						topic.save()
					
					DiscussIndex.objects.create(column=column,
					                            way=WAY_DISCUSS_TOPIC_POST,
					                            discuss=obj,
					                            last_active_time=timezone.now())
					
					if (not FILTER) or (FILTER and is_b):
						Dynamic.objects.create(column=column,
						                       way=WAY_DISCUSS_TOPIC_POST,
						                       content_object=obj)
				else:
					return False
				obj.topics.add(topic)
		
		return obj
	except:
		return False


@login_required
def topics_edit(request):
	'''
	'''
	if request.method == 'POST':
		form = TopicsEditForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			c = data['c']
			topics = data['topics']
			try:
				items = c.split('-')
				t = items[0]
				i = atoi(items[1])
			except:
				raise Http404
			
			obj = topics_change(t, i, topics, request.user)
			
			if obj:
				if isinstance(obj, Link):
					return HttpResponseRedirect(reverse('show_link', 
					                                     args=[obj.id]))
				if isinstance(obj, Discuss):
					return HttpResponseRedirect(reverse('show_discuss', 
					                                     args=[obj.id]))
			try:
				from_url = request.META['HTTP_REFERER']
				return HttpResponseRedirect(from_url)
			except KeyError:
				return HttpResponseRedirect('/')
	
	raise Http404
	
