from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

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
    
    url(r'^message/', include('messages.urls'), name='message'),
    url(r'^remind/', include('remind.urls'), name='remind'),
    url(r'^follow/', include('data.urls'), name='follow'),
    url(r'^operate/', include('votes.urls'), name='vote'),
    
    url(r'^link/', include('links.urls'), name='link'),
    url(r'^discuss/', include('discusses.urls'), name='discuss'),
    url(r'^comment/', include('comments.urls'), name='comment'),
    url(r'^delete/$', 'nng.views.delete', name='delete'),
    
    url(r'^people/', include('profiles.urls'), name='people'),
    url(r'^topic/', include('topics.urls'), name='topic'),
    url(r'^domain/', include('domains.urls'), name='domain'),
    
    url(r'^explore/', include('explore.urls'), name='explore'),
    
    url(r'^post/$', 'nng.views.post', name='post'),
    
    url(r'^admin/', include(admin.site.urls)),
)
