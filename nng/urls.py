from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'nng.views.index', name='homepage'),
    url(r'^login/$', 'accounts.views.user_login', name = 'login'),
    url(r'^logout/$', 'accounts.views.user_logout', name = 'logout'),
    url(r'^regist/$', 'accounts.views.regist', name='regist'),
    url(r'^accounts/', include('accounts.urls'), name='accounts'),
    url(r'^settings/', include('settings.urls'), name='settings'),
    
    url(r'^people/', include('profiles.urls'), name='people'),
    url(r'^message/', include('messages.urls'), name='message'),
    
    url(r'^admin/', include(admin.site.urls)),
)
