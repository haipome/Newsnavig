#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from nng.settings import *
from forms import *
from accounts.models import UserAccount
from django.contrib.auth import authenticate, login, logout
from django.views.generic.simple import direct_to_template

def user_login(request):
	'''
	'''
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('homepage'))
	error_messages = u'你输入的用户名或邮箱和密码不匹配'
	if request.method == "POST":
		form = UserLoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			identification, password, remember_me = (form.cleaned_data['name_or_email'],
			                                         form.cleaned_data['password'],
			                                         form.cleaned_data['remember_me'])
			user = None
			try:
				user = User.objects.get(username=identification)
			except:
				try:
					user = User.objects.get(email=identification)
				except:
					messages.error(request, error_messages)
			if user:
				user = authenticate(username=user.username,
				                    password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
					if remember_me:
						request.session.set_expiry(REMEMBER_ME_WEEKS * 7 * 86400)
					else:
						request.session.set_expiry(0)
					return HttpResponseRedirect(reverse('homepage'))
	form = UserLoginForm()
	return render_to_response('accounts/login_form.html', {'form': form},
	                          context_instance=RequestContext(request))

def user_logout(request):
	'''
	'''
	logout(request)
	return HttpResponseRedirect(reverse('homepage'))

@login_required
def password_change(request):
	'''
	'''
	user = request.user
	form = PasswordChangeForm(user=user)
	if request.method == "POST":
		form = PasswordChangeForm(user=user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, u'密码修改成功')
			return HttpResponseRedirect(reverse('edit_account'))
	return render_to_response('accounts/password_change_form.html', {'form': form},
	                          context_instance=RequestContext(request))

def activate(request, username, confirm_key):
	'''
	'''
	user = UserAccount.objects.confirm_email(username, confirm_key)
	if user:
		messages.success(request, u'你的帐号已经激活，请完善你的个人资料')
		return HttpResponseRedirect(reverse('edit_profile'))
	else:
		return direct_to_template(request, 'accounts/activate_fail.html')

@login_required
def email_change(request):
	'''
	'''
	form = EmailChangeForm()
	user = request.user
	if request.method == "POST":
		form = EmailChangeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if user.email == data['old_email'] and authenticate(
			              username=user.username, password=data['password']):
				user.useraccount.change_email(data['new_email'])
				messages.success(request, 
				u'一封确认邮件已发送到新的邮箱，请点击确认邮件中的链接完成修改。')
				return HttpResponseRedirect(reverse('edit_account'))
	return render_to_response('accounts/email_change_form.html',
	                         {'form': form},
	                           context_instance=RequestContext(request))

def email_confirm(request, username, confirm_key):
	'''
	'''
	user = UserAccount.objects.confirm_email(username, confirm_key)
	if user:
		messages.success(request, u'你的邮箱已更改')
		return HttpResponseRedirect(reverse('edit_account'))
	return direct_to_template(request, 'accounts/email_confirm_fail.html')

