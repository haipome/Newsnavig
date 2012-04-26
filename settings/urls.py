from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
	url(r'^profile/$', views.edit_profile, name='edit_profile'),
	url(r'^email/$', 'accounts.views.email_change', name='edit_email'),
	url(r'^password/$', 'accounts.views.password_change', name='edit_password'),
)
