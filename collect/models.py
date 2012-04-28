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
	
	class Meta:
		ordering = ["-id"]

