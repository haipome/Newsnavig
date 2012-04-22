from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^profile/$', views.edit_profile, name='edit_profile'),
	url(r'^account/$', views.edit_account, name='edit_account'),
	
	# avatar change
	url(r'^avatar/change/$', views.avatar_change, name='avatar_change'),
	
)
