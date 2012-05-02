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
from forms import ProfileForm
from accounts.models import UserAccount
from django.contrib.auth import authenticate, login, logout
from django.views.generic.simple import direct_to_template

@login_required
def edit_profile(request):
	'''
	'''
	user = request.user
	form = ProfileForm()
	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.cleaned_data
			'''
			if len(data['name']) > NAME_MAX_LEN * 3:
				messages.warning(request, u'名号输入过长，被自动截断')
			if len(data['signature']) > SIGNATURE_MAX_LEN * 3:
				messages.warning(request, u'签名输入过长，被自动截断')
			'''
			form.save(user.userprofile, data)
			messages.success(request, u'个人资料修改成功')
		else:
			messages.error(request, u'你的输入有误')
	profile = request.user.userprofile
	return render_to_response('settings/edit_profile.html', 
	                         {'time_limit': PROFILE_NAME_CHANGE_DAYS,
	                          'form': form,
	                          'name': profile.name,
	                          'website': profile.website,
	                          'signature': profile.signature,
	                          'detail': profile.detail,
	                          },
	                           context_instance=RequestContext(request))
