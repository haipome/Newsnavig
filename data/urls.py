from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	
	url(r'^$', views.follow, name='follow_column'),
)
