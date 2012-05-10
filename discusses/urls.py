from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
	url(r'^$', 'nng.views.discuss', name='index_discuss'),
	url(r'^post/$', views.post, name='post_discuss'),
	url(r'^edit/$', views.edit, name='edit_discuss'),
	url(r'^(?P<discuss_id>\d+)/$', views.show_discuss, name="show_discuss"),
	url(r'^(?P<t>\w+)/$', 'nng.views.discuss', name="index_discuss_other"),
)
