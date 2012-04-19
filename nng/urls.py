from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout
from django.views.decorators.csrf import csrf_protect

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'nng.views.index', name='index'),
    url(r'^login/$', csrf_protect(login), {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', csrf_protect(logout), {'template_name': 'accounts/logout.html'}),
    url(r'^accounts/', include('accounts.urls')),
    # url(r'^nng/', include('nng.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
