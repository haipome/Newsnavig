#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from accounts.models import UserAccount
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
	form = UserLoginForm()
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('homepage'))
	error_messages = u'你输入的用户名或邮箱和密码不匹配'
	if request.method == "POST":
		form = UserLoginForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			identification, password, remember_me = (data['name_or_email'],
			                                         data['password'],
			                                         data['remember_me'])
			user = None
			try:
				user = User.objects.get(username__iexact=identification)
			except:
				try:
					user = User.objects.filter(email__iexact=identification)[0]
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
					
					if data['way'] and data['way'] == 'quick':
						try:
							from_url = request.META['HTTP_REFERER']
							return HttpResponseRedirect(from_url)
						except:
							pass
					
					if data['next']:
						return HttpResponseRedirect(data['next'])
					return HttpResponseRedirect(reverse('homepage'))
				else:
					messages.error(request, error_messages)
		else:
			messages.error(request, u'你的输入有误')
	
	next = ''
	if request.method == "GET":
		if 'next' in request.GET and request.GET['next']:
			next = request.GET['next']
	
	return render_to_response('accounts/login_form.html',
	                         {'form': form,
	                          'next': next,},
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
			return HttpResponseRedirect(reverse('edit_profile'))
		else:
			messages.error(request, u'密码修改失败，你的输入有误')
	return render_to_response('accounts/password_change_form.html', {'form': form},
	                          context_instance=RequestContext(request))

def activate(request, username, confirm_key):
	'''
	'''
	user = UserAccount.objects.confirm_email(username, confirm_key)
	if user:
		messages.success(request, u'你的帐号已经激活，请完善你的个人资料')
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		return HttpResponseRedirect(reverse('edit_profile'))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('homepage'))
		else:
			return HttpResponseRedirect(reverse('login'))

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
				
				if user.useraccount.change_email(data['new_email']):
					messages.success(request, 
					u'一封确认邮件已发送到新的邮箱，请点击确认邮件中的链接完成修改。')
					return HttpResponseRedirect(reverse('edit_profile'))
				else:
					messages.error(request, u'你输入的新的邮箱已经注册过了')
			else:
				messages.error(request, u'当前登录邮箱和密码输入错误')
		else:
			messages.error(request, u'更改邮箱地址失败，你的输入有误')
	return render_to_response('accounts/email_change_form.html',
	                         {'form': form},
	                           context_instance=RequestContext(request))

def email_confirm(request, username, confirm_key):
	'''
	'''
	user = UserAccount.objects.confirm_email(username, confirm_key)
	if user:
		messages.success(request, u'你的邮箱已更改')
		return HttpResponseRedirect(reverse('edit_profile'))
	else:
		if request.user.is_authenticated():
			return HttpResponseRedirect(reverse('homepage'))
		else:
			return HttpResponseRedirect(reverse('login'))


def regist(request):
	'''
	'''
	form = RegistForm()
	if request.user.is_authenticated():
		logout(request)
	
	regist_success = False
	if request.method == "POST":
		form = RegistForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			if User.objects.filter(username__iexact=data['username']):
				messages.error(request, u'这个用户名已经注册了')
			elif UserAccount.objects.is_email_regist(data['email']):
				messages.error(request, u'这个邮箱已经注册过了')
			elif data['password1'] != data['password2']:
				messages.error(request, u'两次密码输入不一致')
			elif data['agreement'] == False:
				messages.error(request, u'你在注册前需要同意Newnavig的使用协议')
			else:
				username, email, password = (data['username'],
				                             data['email'],
				                             data['password1'])
				new_user = UserAccount.objects.create_user(
				              username, email, password)
				if new_user:
					regist_success = True
				else:
					messages.error(request, u'这个用户名已经注册了')
		else:
			messages.error(request, u'你的输入不完整或有误')
	
	if regist_success:
		return render_to_response('accounts/regist_complete.html',
		                         {'email': data['email']},
		                          context_instance=RequestContext(request))
	else:
		return render_to_response('accounts/regist_form.html', {'form': form},
		                          context_instance=RequestContext(request))


def email_resend(request):
	'''
	'''
	if request.method == "POST":
		form = ResendActiveEmail(request.POST)
		if form.is_valid():
			data = data = form.cleaned_data
			account = get_object_or_404(UserAccount, email_unconfirmed__iexact=data['email'])
			if account.send_confirm_email():
				messages.success(request, u'邮件已经重新发送，请注意查收')
				return render_to_response('accounts/regist_complete.html',
				                         {'email': data['email']},
	                          context_instance=RequestContext(request))
	raise Http404
	
