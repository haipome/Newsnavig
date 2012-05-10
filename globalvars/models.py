from django.db import models

class GlobalVar(models.Model):
	'''
	'''
	content_id = models.IntegerField(default=0)
	
	link_average_votes = models.FloatField(default=0.0)
	discuss_average_votes = models.FloatField(default=0.0)
	comment_average_votes = models.FloatField(default=0.0)
	


from votes.models import Vote
from shares.models import Share
from collect.models import Collect
from django.contrib.contenttypes import generic

class ContentBase(models.Model):
	'''
	'''
	id = models.IntegerField(primary_key=True)
	
	is_visible = models.BooleanField(default=True, db_index=True)
	is_boutique = models.BooleanField(default=False, db_index=True)
	is_can_comment = models.BooleanField(default=True)
	
	n_comment = models.IntegerField(default=0)
	n_collecter = models.IntegerField(default=0)
	n_supporter = models.IntegerField(default=1, db_index=True)
	n_share = models.IntegerField(default=1)
	
	time = models.DateTimeField(auto_now_add=True, db_index=True)
	
	supporters = generic.GenericRelation(Vote)
	shares = generic.GenericRelation(Share)
	collecters = generic.GenericRelation(Collect)
	
	class Meta:
		abstract=True
	
