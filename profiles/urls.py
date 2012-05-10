from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^(?P<username>[0-9A-Za-z]+)/$', views.people, name='people_home'),
    url(r'^(?P<username>[0-9A-Za-z]+)/(?P<t>\w+)/$', views.people, name='people_other'),
)
