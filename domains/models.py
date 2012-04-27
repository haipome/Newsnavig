from django.db import models
from avatars.models import Avatar


class TagProfile(models.Model):
	'''
	'''
	avatar = ForeignKey(Avatar, blank=True)
	detail = models.TextField(blank=True)
	creat_time = models.DateTimeField(auto_now_add=True)
	
	n_links = models.IntegerField(default=0)
	
	class Meta:
		abstract = True

class Domain(TagProfile):
	'''
	'''
	domain = models.CharField(max_length=64, db_index=True)
	name = models.CharField(max_length=30, blank=True)
	
	def __unicode__(self):
		return self.domain + ': ' + self.name
	
	def get_name(self):
		if self.name:
			return self.name
		else:
			return self.domain
