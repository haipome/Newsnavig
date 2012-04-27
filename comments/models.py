from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Comment(models.Model):
	'''
	'''
	user = models.ForeignKey(User, related_name="user_comments")
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	
	content_type=models.ForeignKey(ContentType, related_name='comments_list')
	object_id = models.PositiveIntegerField()
	reply = generic.GenericForeignKey('content_type', 'object_id')
	
	def __unicode__(self):
		return self.user.username
