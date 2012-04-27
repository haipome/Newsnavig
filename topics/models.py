from django.db import models
from django.contrib.auth.models import User
from domians.models import Domain, TagProfile

class Topic(TagProfile):
	'''
	'''
	name = models.CharField(max_length=30, db_index=True)
	
	users = models.ManyToManyField(User,
	                               through='TopicUserShip',
	                               related_name='user_topics')
	domains = models.ManyToManyField(Domain,
	                                 through='TopicDomainShip',
	                                 related_name='domain_topics')



class TopicUserShip(models.Model):
	'''
	'''
	topic = models.ForeignKey(Topic)
	user = models.ForeignKey(User)
	n_links = models.IntegerField(default=0)
	last_active_time = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering=['-n_links']

class TopicDomainShip(models.Model):
	'''
	'''
	topic = models.ForeignKey(Topic)
	domain = models.ForeignKey(Domain)
	n_links = models.IntegerField(default=0)
	last_active_time = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering=['-n_links']

