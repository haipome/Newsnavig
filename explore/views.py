#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from nng.settings import *
from django.utils.timezone import now
from string import atoi
from links.models import Link
from discusses.models import Discuss
from comments.models import Comment
from profiles.models import UserProfile
from data.models import UserData
from topics.models import Topic
from domains.models import Domain
import datetime

def index(request):
	return HttpResponseRedirect(reverse('explore_link'))


def process_pager(request, limit=True, max_page=MESSAGES_PER_PAGE):
	'''
	'''
	page = 1
	if request.method == 'GET':
		if 'p' in request.GET and request.GET['p']:
			page = atoi(request.GET['p'])
	if limit and page > MAX_PAGE_NUMBER:
		page = MAX_PAGE_NUMBER
	if page != 1:
		pre_page = page - 1
	else:
		pre_page = False
	if limit:
		if page < MAX_PAGE_NUMBER:
			next_page = page + 1
		else:
			next_page = False
	else:
		next_page = page + 1
	
	s = (page - 1) * max_page
	e = s + max_page
	
	return (pre_page, next_page, s, e)

def link(request, t='hot'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	if t == 'hot':
		oneday = datetime.timedelta(days=1)
		start_time = now() - oneday
		links = Link.objects.filter(
		        is_visible=True).filter(
		        time__gt=start_time).order_by(
		        '-n_supporter', 'id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics', 'domain')
	elif t == 'super':
		links = Link.objects.filter(
		        is_visible=True).filter(
		        is_boutique=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics', 'domain')
	elif t == 'new':
		links = Link.objects.filter(
		        is_visible=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics', 'domain')
	else:
		raise Http404
	
	if len(links) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('explore/link.html',
	                         {'links': links,
	                          't':t,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))
	
	
def discuss(request, t='hot'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	if t == 'hot':
		oneday = datetime.timedelta(days=1)
		start_time = now() - oneday
		discusses = Discuss.objects.filter(
		        is_visible=True).filter(
		        time__gt=start_time).order_by(
		        '-n_supporter', 'id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics')
	elif t == 'super':
		discusses = Discuss.objects.filter(
		        is_visible=True).filter(
		        is_boutique=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics')
	elif t == 'new':
		discusses = Discuss.objects.filter(
		        is_visible=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar', 'topics')
	else:
		raise Http404
	
	if len(discusses) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('explore/discuss.html',
	                         {'discusses': discusses,
	                          't':t,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))
	

def comment(request, t='hot'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request)
	
	if t == 'hot':
		oneday = datetime.timedelta(days=1)
		start_time = now() - oneday
		comments = Comment.objects.filter(
		        is_visible=True).filter(
		        time__gt=start_time).order_by(
		        '-n_supporter', 'id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar',
		       'content_object__domain',
		       'parent_comment')
	elif t == 'super':
		comments = Comment.objects.filter(
		        is_visible=True).filter(
		        is_boutique=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar',
		       'content_object__domain',
		       'parent_comment')
	elif t == 'new':
		comments = Comment.objects.filter(
		        is_visible=True).order_by(
		        '-id').all(
		        )[s:e].prefetch_related(
		       'user__userprofile__avatar',
		       'content_object__domain',
		       'parent_comment')
	else:
		raise Http404
	
	if len(comments) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('explore/comment.html',
	                         {'comments': comments,
	                          't':t,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))
	

def user(request, t='hot'):
	'''
	'''
	if t == 'hot':
		users = UserData.objects.order_by(
		        '-this_month_vote', 'id').all(
		        )[:MESSAGES_PER_PAGE].prefetch_related(
		        'user__userprofile__avatar', 'user__userprofile__columns')
	elif t == 'new':
		users = UserData.objects.order_by(
		        '-id').all(
		        )[:MESSAGES_PER_PAGE].prefetch_related(
		        'user__userprofile__avatar', 'user__userprofile__columns')
	
	return render_to_response('explore/user.html',
	                         {'users': users,
	                          't':t,},
	                           context_instance=RequestContext(request))

def topic(request, t='hot'):
	'''
	'''
	if t == 'hot':
		topics = Topic.objects.order_by(
		        '-n_links', 'id').all(
		        )[:MESSAGES_PER_PAGE * 10]
	elif t == 'new':
		topics = Topic.objects.order_by(
		        '-id').all(
		        )[:MESSAGES_PER_PAGE * 10]
	
	return render_to_response('explore/topic.html',
	                         {'topics': topics,
	                          't':t,},
	                           context_instance=RequestContext(request))

def domain(request, t='hot'):
	'''
	'''
	if t == 'hot':
		domains = Domain.objects.order_by(
		        '-n_links', 'id').all(
		        )[:MESSAGES_PER_PAGE * 10]
	elif t == 'new':
		domains = Domain.objects.order_by(
		        '-id').all(
		        )[:MESSAGES_PER_PAGE * 10]
	
	return render_to_response('explore/domain.html',
	                         {'domains': domains,
	                          't':t,},
	                           context_instance=RequestContext(request))
	
	
