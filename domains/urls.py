from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^(?P<domain_name>[\w.]+)/edit/$', views.edit, name='domain_edit'),
    url(r'^(?P<domain_name>[\w.]+)/$', views.domain, name='domain_home'),
    url(r'^(?P<domain_name>[\w.]+)/(?P<t>[\w-]+)/$', views.domain, name='domain_other'),
)
