#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from topics.models import Topic
from forms import TopicEditForm
from django.http import Http404

def topic(request, topic_name):
	'''
	'''
	topic = get_object_or_404(Topic, name__iexact=topic_name)
	column = topic.get_column()
	
	has_followed = False
	if request.user.is_authenticated():
		if column in request.user.userdata.follows.all():
			has_followed = True
	
	return render_to_response('topic/topic_home.html',
	                         {'topic': topic,
	                          'has_followed': has_followed,
	                          'column': column,},
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
	
