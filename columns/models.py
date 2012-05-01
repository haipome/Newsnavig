from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Column(models.Model):
	'''
	'''
	secret_id = models.CharField(max_length=20, db_index=True)
	
	content_type = models.ForeignKey(ContentType, related_name="column_type")
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	time = models.DateTimeField(auto_now_add=True)
	
	n_followers = models.IntegerField(default=0)

