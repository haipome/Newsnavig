#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from columns.models import Column
from remind.utils import creat_remind
from profiles.models import UserProfile
from nng.settings import REMIND_NEW_FOLLOWER
from topics.models import Topic
from domains.models import Domain

def follow(request):
	'''
	'''
	user = request.user
	if not user.is_authenticated():
		return HttpResponse('needlogin')
	c = None
	if request.method == 'GET':
		if 'c' in request.GET and request.GET['c']:
			c = request.GET['c']
		if c:
			try:
				column = Column.objects.get(secret_id__exact=c)
			except:
				pass
			else:
				if column.content_object == user:
					return HttpResponse('False')
				data = user.userdata
				if column not in data.follows.all():
					data.n_follows += 1
					data.follows.add(column)
					column.n_followers += 1
					if isinstance(column.content_object, UserProfile):
						creat_remind(column.content_object.user,
						             user,
						             REMIND_NEW_FOLLOWER)
						
						data.n_follows_user += 1
					elif isinstance(column.content_object, Topic):
						data.n_follows_topic += 1
					elif isinstance(column.content_object, Domain):
						data.n_follows_domain += 1
					else:
						pass
						
				else:
					data.n_follows -= 1
					data.follows.remove(column)
					column.n_followers -= 1
					if isinstance(column.content_object, UserProfile):
						data.n_follows_user -= 1
					elif isinstance(column.content_object, Topic):
						data.n_follows_topic -= 1
					elif isinstance(column.content_object, Domain):
						data.n_follows_domain -= 1
					else:
						pass
				data.save()
				column.save()
				
				return HttpResponse('success')
	
	return HttpResponse('False')
		
