from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	url(r'^$', views.remind, name='remind_un_read'),
	url(r'^all/$', views.remind_all, name='remind_all'),
)
