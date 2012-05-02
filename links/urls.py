from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
	url(r'^post/$', views.post, name='post_link')
)
