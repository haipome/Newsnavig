#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from data.utils import get_follows
from explore.views import process_pager
from nng.settings import MESSAGES_PER_PAGE


def people_follows(request, people):
	'''
	'''
	follows = get_follows(people)
	
	user = request.user
	has_followed = False
	if request.user.is_authenticated() and user != people:
		if follows[4] in request.user.userdata.follows.all():
			has_followed = True
	
	follows.append(has_followed)
	
	followers = follows[4].column_followers.all(
	            )[:MESSAGES_PER_PAGE].prefetch_related(
	            'user__userprofile__avatar')
	follows.append(followers)
	
	return follows

def people(request, username, t='links'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request, limit=False)
	
	people = get_object_or_404(User, username__iexact=username)
	
	follows = people_follows(request, people)
	
	datas = []
	if t == 'followees':
		datas = follows[1][s:e]
	elif t == 'followers':
		followers_d = follows[4].column_followers.all(
		              )[s:e].prefetch_related(
		              'user__userprofile__avatar',
		              'user__userprofile__columns',)
		datas =[]
		for d in followers_d:
			datas.append((d.user.userprofile,
			              d.user.userprofile.columns.all()[0]))
	
	elif t == 'topics':
		datas = follows[2][s:e]
	elif t == 'domains':
		datas = follows[3][s:e]
	else:
		pass
	
	if t == 'followees' or t == 'followers' or t == 'topics' or t == 'domains':
		if len(datas) < MESSAGES_PER_PAGE:
			next_page = False
		
		return render_to_response('people/follows.html',
		                         {'people': people,
		                          'follows': follows,
		                          't': t,
		                          'datas': datas,
		                          'pre': pre_page,
		                          'next': next_page,},
		                           context_instance=RequestContext(request))
	
	if t == 'links':
		datas = people.user_links.filter(is_visible=True).all(
		        )[s:e].prefetch_related(
		        'domain', 'topics')
	elif t == 'discusses':
		datas = people.user_discusses.filter(is_visible=True).all(
		        )[s:e].prefetch_related(
		        'topics')
	elif t == 'comments':
		datas = people.user_comments.filter(is_visible=True).all(
		        )[s:e].prefetch_related(
		        'content_object', 'parent_comment')
	elif t == 'shares':
		datas = people.user_shares.all()[s:e].prefetch_related(
		        'content_object__domain',
		        'content_object__user__userprofile',
		        'comment_object__domain', )
	elif t == 'collections' and people == request.user:
		datas = people.user_collections.all()[s:e].prefetch_related(
		        'content_object__domain',
		        'content_object__user__userprofile',
		        'comment_object__domain', )
	else:
		raise Http404
	
	if len(datas) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('people/homepage.html',
	                         {'people': people,
	                          'follows': follows,
	                          't': t,
	                          'datas': datas,
	                          'pre': pre_page,
	                          'next': next_page,},
	                           context_instance=RequestContext(request))
	

