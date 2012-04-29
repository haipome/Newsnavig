from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Comment(models.Model):
	'''
	'''
	id = models.IntegerField(primary_key=True)
	
	is_visible = models.BooleanField(default=True)
	is_boutique = models.BooleanField(default=False)
	is_can_comment = models.BooleanField(default=True)
	
	user = models.ForeignKey(User, related_name="user_comments")
	time = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	
	parent_comment = models.ForeignKey('self', null=True, blank=True,
	                                   related_name='follow_comment')
	
	content_type=models.ForeignKey(ContentType, related_name='comments_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	
	n_reply = models.IntegerField(default=0)
	n_collecter = models.IntegerField(default=0)
	n_supporter = models.IntegerField(default=1)
	n_shares = models.IntegerField(default=1)
	
	
	def __unicode__(self):
		return self.user.username + ' ' + str(self.n_reply)
	
	class Meta:
		ordering = ["-id"]
