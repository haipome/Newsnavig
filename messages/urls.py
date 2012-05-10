from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^$', views.inbox, name='message_inbox'),
    url(r'^send/$', views.send, name='message_send'),
    url(r'^choose/$', views.choose, name='message_choose'),
    url(r'^delete/$', views.delete, name="message_delete"),
    url(r'^(?P<contact_id>[0-9]+)/$', views.conversation,
        name="conversation"),
)
