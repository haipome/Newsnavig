from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^(?P<domain_name>.+)/edit/$', views.edit, name='domain_edit'),
    url(r'^(?P<domain_name>.+)/$', views.domain, name='domain_home'),
)
