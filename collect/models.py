from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Collect(models.Model):
	'''
	'''
	content_type=models.ForeignKey(ContentType, related_name="collect_type")
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	user = models.ForeignKey(User, related_name="user_collections")
	time = models.DateTimeField(auto_now_add=True)
	
	way = models.CharField(max_length=1) # 'l' or 'd' or 'c'
	
	# optimization for comment
	comment_type = models.ForeignKey(ContentType, related_name="collect_comment", null=True)
	comment_obj_id = models.PositiveIntegerField(null=True)
	comment_object = generic.GenericForeignKey('comment_type', 'comment_obj_id')
	
	class Meta:
		ordering = ["-id"]

