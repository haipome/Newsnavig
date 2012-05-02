from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^(?P<topic_name>.+)/edit/$', views.edit, name='topic_edit'),
    url(r'^(?P<topic_name>.+)/$', views.topic, name='topic_home'),
)
