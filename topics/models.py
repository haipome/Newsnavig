from django.db import models
from django.contrib.auth.models import User
from domains.models import Domain, TagProfile
from columns.utils import create_column

class Topic(TagProfile):
	'''
	'''
	n_discusses = models.IntegerField(default=0)
	n_discusses_boutiques = models.IntegerField(default=0)
	
	link_average_votes = models.FloatField(default=0.0)
	discuss_average_votes = models.FloatField(default=0.0)
	comment_average_votes = models.FloatField(default=0.0)
	
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
			return create_column(self)
	
	def get_absolute_url(self):
		return '/%s/%s/' % ('topic', self.name)
	
	def get_name(self):
		return self.name

class TopicBaseShip(models.Model):
	'''
	'''
	topic = models.ForeignKey(Topic)
	n_links = models.IntegerField(default=0)
	n_comments = models.IntegerField(default=0)
	votes = models.IntegerField(default=0)
	
	last_active_time = models.DateTimeField(auto_now_add=True)
	
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

