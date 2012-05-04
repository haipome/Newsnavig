from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
	url(r'^post/$', views.post, name='post_discuss'),
	url(r'^(?P<discuss_id>\d+)/$', views.show_discuss, name="show_discuss"),
)
