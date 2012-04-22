#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from nng.settings import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
import views

urlpatterns = patterns('',
	
	# password change
	url(r'^password/change/$', views.password_change, name='password_change'),
	
	# password reset
	url(r'^password/reset/$',
	    auth_views.password_reset,
	    {'template_name': 'accounts/password_reset_form.html',
	     'email_template_name': 'accounts/emails/password_reset_message.txt',
	     'subject_template_name': 'accounts/emails/password_reset_subject.txt',
	     'from_email': ACCOUNT_CONFIRM_FROM_EMAIL},
	     name='password_reset'),
	url(r'^password/reset/done/$',
	    auth_views.password_reset_done,
	    {'template_name': 'accounts/password_reset_done.html'},
	    name='password_reset_done'),
	url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
	    auth_views.password_reset_confirm,
	    {'template_name': 'accounts/password_reset_confirm_form.html'},
	    name='password_reset_confirm'),
	url(r'^password/reset/confirm/complete/$',
	    auth_views.password_reset_complete,
	    {'template_name': 'accounts/password_reset_complete.html'}),
	
	# activate
	url(r'^activate/(?P<username>[\.\w]+)/(?P<confirm_key>\w+)/$',
	    views.activate,
	    name='activate'),
	
	# change email
	url(r'^email/change/$',
	    views.email_change,
	    name='email_change'),
	url(r'^email/confirm/(?P<username>[\.\w]+)/(?P<confirm_key>\w+)/$',
	    views.email_confirm,
	    name='email_confirm'),
)
