#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from topics.models import TopicUserShip
from topics.utils import get_hot_topic
from nng.settings import LATEST_TOPICS_NUMBER
from dynamic.utils import get_dynamics
from dynamic.models import Dynamic
from discusses.utils import get_discusses
from explore.views import process_pager
from datetime import date
from dateutil import tz
from nng.settings import TIME_ZONE, MESSAGES_PER_PAGE
from data.utils import get_follows
from links.models import Link
from discusses.models import Discuss, DiscussIndex
from comments.models import Comment
from shares.models import Share
from collect.models import Collect
from string import atoi
from comments.utils import del_comment
from discusses.utils import del_discuss
from links.utils import del_link
from nng.settings import *

def get_user_topics(user):
	if user.is_authenticated():
		return user.user_topics.order_by(
		             '-topicusership__last_active_time')[:LATEST_TOPICS_NUMBER]
	else:
		return None


def index(request):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	if pre_page:
		page = pre_page + 1
	else:
		page = 1
	today = date.today()
	local = tz.gettz(TIME_ZONE)
	
	user = request.user
	if not user.is_authenticated():
		
		topics = get_hot_topic(MESSAGES_PER_PAGE)
		
		d_types = ['a', 'e', 'h', 'i']
		dynamics = Dynamic.objects.filter(
		           is_visible=True).filter(
		           way__in=d_types).order_by(
		           '-id').all(
		           )[s:e].prefetch_related(
		           'content_object__user__userprofile__avatar',
		           'content_object__domain',
		           'column__content_object',
		           'comment_object__domain',)
		
		for d in dynamics:
			d.time = d.time.astimezone(local)
		
		if len(dynamics) < MESSAGES_PER_PAGE:
			next_page = False
		
		return render_to_response('dynamic.html', 
		                         {'dynamics':dynamics,
		                          'topics': topics,
		                          'today': today,
		                          'pre': pre_page,
		                          'next': next_page,},
		                           context_instance=RequestContext(request))
	
	user_topics = get_user_topics(user)
	
	follow = get_follows(user)
	dynamics, has_next_page = get_dynamics(user, follow[0], page)
	
	for d in dynamics:
		d.time = d.time.astimezone(local)
	
	if not has_next_page:
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
	if pre_page:
		page = pre_page + 1
	else:
		page = 1
	today = date.today()
	local = tz.gettz(TIME_ZONE)
	
	if not user.is_authenticated() and t == 'follow':
		t = 'all'
		topics = get_hot_topic(MESSAGES_PER_PAGE)
		
		discusses = Discuss.objects.filter(
		            is_visible=True).order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'user__userprofile__avatar',
		            'last_active_user__userprofile',)
		
		if len(discusses) < MESSAGES_PER_PAGE:
			next_page = False
		
		for d in discusses:
			if d.last_active_time:
				d.last_active_time = d.last_active_time.astimezone(local)
		
		return render_to_response('discuss.html',
		                         {'discusses':discusses,
		                          'topics': topics,
		                          't': t,
		                          'today': today,
		                          'pre': pre_page,
		                          'next': next_page,},
		                           context_instance=RequestContext(request))
		
	if not user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	
	user_topics = get_user_topics(user)
	follow = get_follows(user)
	
	if t == 'follow':
		discusses, has_next_page = get_discusses(user, follow[0], page)
		if not has_next_page:
			next_page = False
	elif t == 'reply':
		discusses = user.userdata.discusses.order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'user__userprofile__avatar',
		            'last_active_user__userprofile',)
		if len(discusses) < MESSAGES_PER_PAGE:
			next_page = False
	elif t == 'me':
		discusses = user.user_discusses.order_by(
		            '-last_active_time').all(
		            )[s:e].prefetch_related(
		            'user__userprofile__avatar',
		            'last_active_user__userprofile',)
		if len(discusses) < MESSAGES_PER_PAGE:
			next_page = False
	else:
		raise Http404
	
	for d in discusses:
		if d.last_active_time:
			d.last_active_time = d.last_active_time.astimezone(local)
	
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
	
	if request.method == 'GET':
		if 'topic' in request.GET and request.GET['topic']:
			topic = request.GET['topic']
		else:
			topic = ''
		if 'type'  in request.GET and request.GET['type']:
			t = request.GET['type']
		else:
			t = 'link'
	
	if t != 'link' and t != 'discuss':
		t = 'link'
	
	try:
		from_url = request.META['HTTP_REFERER']
	except:
		from_url = None
	
	return render_to_response('post.html',
	                         {'user_topics': user_topics,
	                          'from_url': from_url,
	                          't': t,
	                          'topic': topic,},
	                           context_instance=RequestContext(request))


@login_required
def delete(request):
	'''
	'''
	user = request.user
	if request.method == 'GET':
		if 'c' in request.GET and request.GET['c']:
			c = request.GET['c']
			
			try:
				items = c.split('-')
				t = items[0]
				i = atoi(items[1])
			except:
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
			elif t == 's' and i:
				try:
					obj = Share.objects.get(user=user, object_id=i)
				except:
					raise Http404
			elif t == 'f' and i:
				try:
					obj = Collect.objects.get(user=user, object_id=i)
				except:
					raise Http404
			else:
				raise Http404
			
			if t == 's' or t == 'f':
				
				if t == 's':
					obj.content_object.n_share -= 1
					obj.content_object.save()
					user.userdata.n_shares -= 1
					user.userdata.save()
					
					Dynamic.objects.filter(
					        column=user.userprofile.get_column()).filter(
					        object_id=obj.content_object.id).update(
					        is_visible=False)
					
				elif t == 'f':
					obj.content_object.n_collecter -= 1
					obj.content_object.save()
					user.userdata.n_collections -= 1
					user.userdata.save()
				else:
					pass
				
				obj.delete()
				try:
					from_url = request.META['HTTP_REFERER']
					return HttpResponseRedirect(from_url)
				except KeyError:
					return HttpResponseRedirect(reverse('homepage'))
			
			
			if obj.is_visible == False:
				raise Http404
			
			if user == obj.user and obj.n_comment == 0:
				Dynamic.objects.filter(object_id=obj.id).update(
				                is_visible=False)
				
				obj.is_visible = False
				obj.save()
				
				if t == 'c':
					del_comment(obj)
				
				if t == 'd':
					del_discuss(obj)
					
					DiscussIndex.objects.filter(
					             discuss_id=obj.id).update(
					             is_visible=False)
				
				if t == 'l':
					del_link(obj)
				
				if t == 'l' or t == 'd':
					return HttpResponseRedirect(reverse('homepage'))
				elif t == 'c':
					if isinstance(obj.content_object, Link):
						return HttpResponseRedirect(
						       reverse('links.views.show_link',
						       args=[str(obj.content_object.id)]))
					elif isinstance(obj.content_object, Discuss):
						return HttpResponseRedirect(
						       reverse('discusses.views.show_discuss',
						       args=[str(obj.content_object.id)]))
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		return HttpResponseRedirect(reverse('homepage'))
	
