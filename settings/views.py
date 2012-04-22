#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from nng.settings import *
from forms import DetailChangeForm, NameChangeForm, AvatarChangeForm
from accounts.models import UserAccount
from django.contrib.auth import authenticate, login, logout
from django.views.generic.simple import direct_to_template

@login_required
def edit_profile(request):
	'''
	'''
	if request.method == "POST":
		form = DetailChangeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			form.save(request.user.userprofile, data)
			messages.success(request, u'个人资料修改成功')
	profile = request.user.userprofile
	form = DetailChangeForm(initial={'website': profile.website,
	                                 'signature': profile.signature,
	                                 'detail': profile.detail,})
	return render_to_response('settings/edit_profile.html', 
	                         {'time_limit': PROFILE_NAME_CHANGE_DAYS,
	                          'form': form},
	                           context_instance=RequestContext(request))
@login_required
def edit_account(request):
	return render_to_response('settings/edit_account.html', 
	                          context_instance=RequestContext(request))

@login_required
def avatar_change(request):
	'''
	'''
	user = request.user
	form = AvatarChangeForm()
	if request.method == "POST":
		form = AvatarChangeForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(user, request)
			messages.success(request, u'头像修改成功')
			return HttpResponseRedirect(reverse('edit_profile'))
	return render_to_response('settings/avatar_form.html', {'form': form},
	                          context_instance=RequestContext(request))

@login_required
def name_change(request):
	'''
	'''
	user = request.user
	if not user.userprofile.is_can_change_name():
		messages.warning(request, u'%s 天内只能修改一次名号' % 
		                 str(PROFILE_NAME_CHANGE_DAYS))
		return HttpResponseRedirect(reverse('profile'))
	form = NameChangeForm()
	if request.method == "POST":
		form = NameChangeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if user.userprofile.change_name(form.cleaned_data['new_name']):
				messages.success(request, u'你的名号已成功修改')
			else:
				messages.error(request, u'名号修改失败')
			return HttpResponseRedirect(reverse('edit_profile'))
	return render_to_response('accounts/name_change_form.html',
	                         {'form': form},
	                           context_instance=RequestContext(request))

