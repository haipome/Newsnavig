from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	
	url(r'^$', views.operate, name='user_operate'),
)
