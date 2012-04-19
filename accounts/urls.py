#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^profile/$', 'accounts.views.profile'),
)
