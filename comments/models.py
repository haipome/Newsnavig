from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from globalvars.models import ContentBase
from domains.models import Domain

class Comment(ContentBase):
	'''
	'''
	user = models.ForeignKey(User, related_name="user_comments")
	
	content = models.TextField()
	way = models.CharField(max_length=1) # 'l' or 'd'
	
	parent_comment = models.ForeignKey('self', null=True, blank=True,
	                                   related_name='follow_comments')
	
	content_type=models.ForeignKey(ContentType, related_name='comments_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	domain = models.ForeignKey(Domain, related_name="domain_comments", null=True, blank="true") # not user
	comments = generic.GenericRelation('self')
	
	def __unicode__(self):
		return self.user.username + ' ' + str(self.n_supporter)
	
	class Meta:
		ordering = ["-id"]
	
	def get_absolute_url(self):
		return '/%s/%s/' % ('comment', str(self.id))
	
