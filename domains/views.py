#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from domains.models import Domain
from forms import DomainEditForm


def domain(request, domain_name):
	'''
	'''
	d = get_object_or_404(Domain, domain__iexact=domain_name)
	column = d.get_column()
	
	has_followed = False
	if request.user.is_authenticated():
		if column in request.user.userdata.follows.all():
			has_followed = True
	
	return render_to_response('domain/domain_home.html',
	                         {'domain': d,
	                          'has_followed': has_followed,
	                          'column': column,},
	                           context_instance=RequestContext(request))
	

def edit(request, domain_name):
	'''
	'''
	if request.method == 'POST':
		form = DomainEditForm(request.POST, request.FILES)
		if form.is_valid():
			d = get_object_or_404(Domain, domain__iexact=domain_name)
			form.save(d)
			
	try:
		from_url = request.META['HTTP_REFERER']
		return HttpResponseRedirect(from_url)
	except KeyError:
		return Http404()
	
