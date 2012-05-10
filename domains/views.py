#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from domains.models import Domain
from forms import DomainEditForm
from explore.views import process_pager
from nng.settings import MESSAGES_PER_PAGE
from data.models import FollowShip

def domain(request, domain_name, t='links'):
	'''
	'''
	pre_page, next_page, s, e = process_pager(request, limit=False)
	
	domain = get_object_or_404(Domain, domain__iexact=domain_name)
	column = domain.get_column()
	
	followers_ship = FollowShip.objects.filter(
	                 column=column).all(
	                 )[:MESSAGES_PER_PAGE].prefetch_related(
	                 'userdata__user__userprofile__avatar')
	
	followers = [obj.userdata.user.userprofile for obj in followers_ship]
	
	if t == 'links':
		datas = domain.domain_links.filter(
		        is_visible=True).all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar', 'domain', 'topics')
	elif t == 'super':
		datas = domain.domain_links.filter(
		        is_visible=True).filter(
		        is_boutique=True).all(
		        )[s:e].prefetch_related(
		        'user__userprofile__avatar', 'domain', 'topics')
	
	elif t == 'followers':
		followers_ship = FollowShip.objects.filter(
		                 column=column).all(
		                 )[s:e].prefetch_related(
		                 'userdata__user__userprofile__avatar')
		
		datas = [(obj.userdata.user.userprofile, \
		          obj.column) for obj in followers_ship]
	else:
		raise Http404
	
	if len(datas) < MESSAGES_PER_PAGE:
		next_page = False
	
	return render_to_response('domain/domain_home.html',
	                         {'domain': domain,
	                          'column': column,
	                          't': t,
	                          'followers': followers,
	                          'datas': datas,},
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
		raise Http404
	
