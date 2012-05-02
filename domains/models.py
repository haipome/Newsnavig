from django.db import models
from avatars.models import Avatar
from django.contrib.contenttypes import generic
from columns.models import Column
from nng.settings import NAME_MAX_LEN

class TagProfile(models.Model):
	'''
	'''
	name = models.CharField(max_length=NAME_MAX_LEN, blank=True, db_index=True)
	
	columns = generic.GenericRelation(Column)
	
	avatar = models.ForeignKey(Avatar, blank=True, null=True)
	detail = models.TextField(blank=True)
	create_time = models.DateTimeField(auto_now_add=True)
	
	n_links = models.IntegerField(default=0, db_index=True)
	n_links_boutiques = models.IntegerField(default=0)
	
	class Meta:
		abstract = True

class Domain(TagProfile):
	'''
	'''
	domain = models.CharField(max_length=64, db_index=True)
	# will create a same name topic
	
	def __unicode__(self):
		return '%s: %s' % (self.domain, self.name)
	
	def get_name(self):
		if self.name:
			return self.name
		else:
			return self.domain
	
	def get_domain_url(self):
		return r'http://' + self.domain
	
	def get_column(self):
		try:
			return self.columns.all()[0]
		except:
			return None
		
	def get_absolute_url(self):
		return '/%s/%s/' % ('domain', self.domain)
	
