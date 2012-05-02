from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from data.models import ContentBase

class Comment(ContentBase):
	'''
	'''
	user = models.ForeignKey(User, related_name="user_comments")
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	
	parent_comment = models.ForeignKey('self', null=True, blank=True,
	                                   related_name='follow_comment')
	
	content_type=models.ForeignKey(ContentType, related_name='comments_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	way = models.CharField(max_length=1)
	
	comments = generic.GenericRelation('self')
	
	def __unicode__(self):
		return self.user.username + ' ' + str(self.n_reply)
	
	class Meta:
		ordering = ["-id"]
	
	def get_absolute_url(self):
		return '/%s/%s/' % ('comment', str(self.id))
