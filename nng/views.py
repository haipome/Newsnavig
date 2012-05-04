#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from topics.models import TopicUserShip
from nng.settings import LATEST_TOPICS_NUMBER

def get_user_topics(user):
	if user.is_authenticated():
		return user.user_topics.order_by(
		             '-topicusership__last_active_time')[:LATEST_TOPICS_NUMBER]
	else:
		return None


def index(request):
	'''
	'''
	user = request.user
	user_topics = get_user_topics(user)
	
	return render_to_response('index.html', 
	                         {'user_topics': user_topics,},
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
