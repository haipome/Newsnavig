from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Vote(models.Model):
	'''
	'''
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)
	
	content_type=models.ForeignKey(ContentType, related_name='vote_type')
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
