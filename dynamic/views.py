#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from columns.models import Column
from models import Dynamic


def dynamic(request):
	'''
	'''
	user = request.user
	
	columns = user.userdata.follows.all().prefetch_related(
	         'content_object__avatar')
	
	follows = [entry for entry in columns]
	user_self = user.userprofile.get_column()
	if user_self not in follows:
		follows.append(user.userprofile.get_column())
	
	dynamics = Dynamic.objects.filter(
	           colum__in=follows).order_by(
	           '-id').prefetch_related(
	           'content_object')
