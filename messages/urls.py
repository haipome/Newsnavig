from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^send/$', views.send, name='message_send'),
    url(r'^inbox/$', views.inbox, name='message_inbox'),
    url(r'^inbox/(?P<contact_id>[0-9]+)/$', views.conversation,
        name="conversation")
)
