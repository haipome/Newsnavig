from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from columns.models import Column

class Dynamic(models.Model):
	'''
	'''
	is_visible = models.BooleanField(default=True)
	
	column = models.ForeignKey(Column, related_name="column_dynamic")
	time = models.DateTimeField(auto_now_add=True)
	
	way = models.CharField(max_length=1)
	
	content_type=models.ForeignKey(ContentType, related_name='dynamic_type')
	object_id = models.PositiveIntegerField(db_index=True)
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	
	class Meta:
		ordering=["-id"]
