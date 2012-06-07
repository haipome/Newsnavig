#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import DiscussPostForm, DiscussEditForm
from discusses.utils import post_discuss
from django.contrib import messages
from nng.settings import *
from django.core.urlresolvers import reverse
from links.views import topics_get
from string import atoi
from models import Discuss
from comments.utils import comment_sort
from comments.models import Comment
from nng.views import get_user_topics
from topics.views import topics_change

@login_required
def post(request):
	'''
	'''
	user = request.user
	
	if request.method == 'POST':
		form = DiscussPostForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			title, detail, topics_n = (data['title'], data['detail'],
			        data['topics'].split(' '))
			
			title = title[:TITLE_MAX_LEN]
			topics = topics_get(topics_n)
			
			d = post_discuss(user, title, detail, topics)
			
			if not d:
				messages.error(request, u'发布失败')
			
			if data['goback'] or not d:
				try:
					from_url = request.META['HTTP_REFERER']
					return HttpResponseRedirect(from_url)
				except KeyError:
					pass
			
			return HttpResponseRedirect(reverse('show_discuss', args=[d.id]))
	
	return HttpResponseRedirect(reverse('homepage'))

@login_required
def edit(request):
	user = request.user
	
	if request.method == 'POST':
		form = DiscussEditForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			discuss_id, title, detail = (atoi(data['discuss_id']),
			                             data['title'],
			                             data['detail'] )
			title = title[:TITLE_MAX_LEN]
			topics = data['topics']
			
			try:
				d = Discuss.objects.get(pk=discuss_id)
			except:
				raise Http404
			
			d.title = title
			d.detail = detail
			
			if not topics_change('d', d.id, topics, user):
				pass
			
			d.save()
			
			return HttpResponseRedirect(reverse('show_discuss', args=[d.id]))
	elif request.method  == 'GET':
		if 'c' in  request.GET and request.GET['c']:
			c = atoi(request.GET['c'])
			try:
				d = Discuss.objects.get(pk=c)
			except:
				raise Http404
			
			user_topics = get_user_topics(user)
			
			try:
				from_url = request.META['HTTP_REFERER']
			except:
				from_url = "/"
			
			return render_to_response('discuss/edit.html',
			                         {'d': d,
			                          'from_url': from_url,
			                          'user_topics': user_topics,},
			                           context_instance=RequestContext(request))
	
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		return HttpResponseRedirect(reverse('homepage'))


def show_discuss(request, discuss_id):
	'''
	'''
	discuss = get_object_or_404(Discuss, id=atoi(discuss_id))
	if discuss.is_visible == False:
		raise Http404
	
	comments = discuss.comments.filter(
	           is_visible=True).all(
	           ).select_related(
	           'user__userprofile__avatar')
	
	comments = comment_sort(comments, COMMENT_DEEPS)
	
	return render_to_response('discuss/show_discuss.html',
	                         {'d': discuss,
	                          'comments': comments},
	                         context_instance=RequestContext(request))
	

