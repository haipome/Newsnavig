from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^(?P<topic_name>\w+)/edit/$', views.edit, name='topic_edit'),
    url(r'^(?P<topic_name>\w+)/$', views.topic, name='topic_home'),
    url(r'^(?P<topic_name>\w+)/(?P<t>[\w-]+)/$', views.topic, name='topic_other'),
)
