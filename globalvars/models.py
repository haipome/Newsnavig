from django.db import models

class GlobalVar(models.Model):
	'''
	'''
	content_id = models.IntegerField(default=0)
	
	link_average_votes = models.FloatField(default=0.0)
	discuss_average_votes = models.FloatField(default=0.0)
	comments_average_votes = models.FloatField(default=0.0)
	
