from django.db import models
from django.contrib.auth.models import User
from domains.models import Domain, TagProfile

class Topic(TagProfile):
	'''
	'''
	n_discusses = models.IntegerField(default=0)
	
	users = models.ManyToManyField(User,
	                               through='TopicUserShip',
	                               related_name='user_topics')
	domains = models.ManyToManyField(Domain,
	                                 through='TopicDomainShip',
	                                 related_name='domain_topics')
	
	def __unicode__(self):
		return self.name
	
	def get_column(self):
		try:
			return self.columns.all()[0]
		except:
			return None

class TopicBaseShip(models.Model):
	'''
	'''
	topic = models.ForeignKey(Topic)
	n_links = models.IntegerField(default=0)
	n_comments = models.IntegerField(default=0)
	votes = models.IntegerField(default=0)
	
	last_active_time = models.DateTimeField(auto_now=True)
	
	class Meta:
		abstract=True

class TopicUserShip(TopicBaseShip):
	'''
	'''
	user = models.ForeignKey(User)
	n_discusses = models.IntegerField(default=0)
	
	class Meta:
		ordering=['-votes']

class TopicDomainShip(TopicBaseShip):
	'''
	'''
	domain = models.ForeignKey(Domain)
	class Meta:
		ordering=['-votes']

