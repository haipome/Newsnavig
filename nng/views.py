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
	
	user = request.user
	if not user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	
	user_topics = get_user_topics(user)
	
	follow = get_follows(user)
	dynamics, has_next_page = get_dynamics(user, follow[0], page)
	
	today = date.today()
	local = tz.gettz(TIME_ZONE)
	
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
	if not user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
	
	user_topics = get_user_topics(user)
	follow = get_follows(user)
	
	if pre_page:
		page = pre_page + 1
	else:
		page = 1
	
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
	
	today = date.today()
	local = tz.gettz(TIME_ZONE)
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
	
	try:
		from_url = request.META['HTTP_REFERER']
	except:
		from_url = None
	
	return render_to_response('post.html',
	                         {'user_topics': user_topics,
	                          'from_url': from_url,},
	                           context_instance=RequestContext(request))



def delete(request):
	'''
	'''
	user = request.user
	if request.method == 'GET':
		if 'c' in request.GET and request.GET['c']:
			c = request.GET['c']
			
			items = c.split('-')
			t = items[0]
			i = atoi(items[1])
			
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
				
				obj.is_visible = False
				obj.save()
				if t == 'c':
					user.userdata.n_comments -= 1
					user.userdata.save()
					if obj.parent_comment:
						obj.parent_comment.n_comment -= 1
						obj.parent_comment.save()
					if obj.content_object:
						obj.content_object.n_comment -= 1
						obj.content_object.save()
				
				Dynamic.objects.filter(object_id=obj.id).update(
				                is_visible=False)
				
				if t == 'd':
					user.userdata.n_discusses -= 1
					user.userdata.save()
					DiscussIndex.objects.filter(
					             discuss_id=obj.id).update(
					             is_visible=False)
				
				if t == 'l':
					user.userdata.n_links -= 1
					user.userdata.save()
				
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
