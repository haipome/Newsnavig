from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
	url(r'^post/$', views.post, name='post_comment'),
	url(r'^(?P<comment_id>\d+)/$', views.show_comment, name="show_comment"),
)
