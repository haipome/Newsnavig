#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	url(r'^$', views.index, name="explore_index"),
	url(r'^link/$', views.link, name="explore_link"),
	url(r'^link/(?P<t>\w+)/$', views.link, name="explore_link_other"),
	url(r'^discuss/$', views.discuss, name="explore_discuss"),
	url(r'^discuss/(?P<t>\w+)/$', views.discuss, name="explore_discuss_other"),
	url(r'^comment/$', views.comment, name="explore_comment"),
	url(r'^comment/(?P<t>\w+)/$', views.comment, name="explore_comment_other"),
	url(r'^user/$', views.user, name="explore_user"),
	url(r'^user/(?P<t>\w+)/$', views.user, name="explore_user_other"),
	url(r'^topic/$', views.topic, name="explore_topic"),
	url(r'^topic/(?P<t>\w+)/$', views.topic, name="explore_topic_other"),
	url(r'^domain/$', views.domain, name="explore_domain"),
	url(r'^domain/(?P<t>\w+)/$', views.domain, name="explore_domain_other"),
)
