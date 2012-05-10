from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

class Share(models.Model):
	'''
	'''
	content_type=models.ForeignKey(ContentType, related_name='share_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	way = models.CharField(max_length=1) # 'l' or 'd' or 'c'
	
	user = models.ForeignKey(User, related_name="user_shares")
	time = models.DateTimeField(auto_now_add=True)
	
	# optimization for comment
	comment_type = models.ForeignKey(ContentType, related_name="share_comment", null=True)
	comment_obj_id = models.PositiveIntegerField(null=True)
	comment_object = generic.GenericForeignKey('comment_type', 'comment_obj_id')
	
	class Meta:
		ordering = ["-id"]
