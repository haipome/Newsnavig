#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
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
from django.contrib.contenttypes.models import ContentType
from columns.models import Column
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
		        '-n_supporter', '-id').all(
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
		        '-n_supporter', '-id').all(
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
		        '-n_supporter', '-id').all(
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
	
@login_required
def user(request, t='hot'):
	'''
	'''
	if t == 'hot':
		users = UserData.objects.order_by(
		        '-this_month_vote', '-id').all(
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
		topic_type  = ContentType.objects.get(app_label='topics', model='topic')
		
		topics_c = Column.objects.filter(content_type=topic_type).order_by(
		                                 '-n_followers', '-id').all(
		                                 )[:MESSAGES_PER_PAGE * 10
		                                 ].prefetch_related(
		                                 'content_object')
		topics = []
		for c in topics_c:
			topics.append(c.content_object)
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
		domain_type = ContentType.objects.get(app_label='domains',
		                                      model='domain')
		
		domains_c = Column.objects.filter(content_type=domain_type).order_by(
		                                 '-n_followers', '-id').all(
		                                 )[:MESSAGES_PER_PAGE * 10
		                                 ].prefetch_related(
		                                 'content_object')
		
		domains = []
		for c in domains_c:
			domains.append(c.content_object)
	elif t == 'new':
		domains = Domain.objects.order_by(
		        '-id').all(
		        )[:MESSAGES_PER_PAGE * 10]
	
	return render_to_response('explore/domain.html',
	                         {'domains': domains,
	                          't':t,},
	                           context_instance=RequestContext(request))
	
	
