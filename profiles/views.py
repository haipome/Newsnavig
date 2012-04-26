#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User

def people(request, username):
	'''
	'''
	people = get_object_or_404(User, username__iexact=username)
	return render_to_response('people/homepage.html',
	                         {'people': people},
	                          context_instance=RequestContext(request))
