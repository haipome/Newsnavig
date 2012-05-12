#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from nng.settings import MESSAGES_PER_PAGE
from models import Remind
from django.http import Http404
from string import atoi


def get_unread_remind(user, number=MESSAGES_PER_PAGE):
	'''
	'''
	reminds = Remind.objects.filter(
	          to_user=user).filter(
	          is_read=False).all(
	          )[:number].prefetch_related(
	          'from_user__userprofile', 'comment')
	
	last_id = -1
	for remind in reminds:
		last_id = remind.id
	
	if last_id != -1:
		Remind.objects.filter(to_user=user).filter(id__gte=last_id).update(
		               is_read=True)
	
	l = len(reminds)
	if l:
		user.userdata.un_read_remind -= len(reminds)
	else:
		user.userdata.un_read_remind = 0
	more = user.userdata.un_read_remind
	if user.userdata.un_read_remind < 0:
		user.userdata.un_read_remind = 0
	user.userdata.save()
	
	return (reminds, more)

@login_required
def remind(request):
	'''
	'''
	reminds, more = get_unread_remind(request.user)
	return render_to_response('remind/un_read.html',
	                         {'reminds': reminds,
	                          'more': more,},
	                          context_instance=RequestContext(request))
	

@login_required
def remind_all(request):
	'''
	'''
	user = request.user
	page = 1
	if request.method == 'GET':
		if 'p' in request.GET and request.GET['p']:
			page = atoi(request.GET['p'])
	
	if page != 1 and ((page - 1) * MESSAGES_PER_PAGE) >= user.userdata.n_reminds:
		raise Http404
	
	if page != 0:
		pre_page = page - 1
	else:
		pre_page = False
	if page * MESSAGES_PER_PAGE < user.userdata.n_reminds:
		next_page = page + 1
	else:
		next_page = False
	
	s = (page - 1) * MESSAGES_PER_PAGE
	e = s + MESSAGES_PER_PAGE
	
	reminds = Remind.objects.filter(
	          to_user = user).all(
	          )[s:e].prefetch_related(
	          'from_user__userprofile', 'comment')
	
	
	return render_to_response('remind/all.html',
		                     {'reminds': reminds,
		                      'pre': pre_page,
		                      'next': next_page,},
		                       context_instance=RequestContext(request))
