from django.db import models
from django.contrib.auth.models import User
from domians.models import Domain
from topics.models import Topic

class Link(models.Model):
	'''
	'''
	url = models.URLField(max_length=1000)
	title = models.CharField(max_length=210)
	post_time = models.DateTimeField(auto_now_add=True)
	
	post_user = models.ForeignKey(User, related_name="user_links")
	topics = models.ManyToManyField(Topic, related_name="topic_links")
	domain = models.ForeignKey(Domain, related_name="domain_links")
	
	n_support = models.IntegerField(default=1)
	n_oppose  = models.IntegerField(default=0)
