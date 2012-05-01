from django.db import models
from django.contrib.auth.models import User
from columns.models import Column
from django.contrib.contenttypes import generic
from votes.models import Vote
from shares.models import Share
from collect.models import Collect

class UserData(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	
	n_follows = models.IntegerField(default=0)
	follows = models.ManyToManyField(Column, related_name="column_follower")
	
	honor = models.IntegerField(default=1)
	
	un_read_messages = models.IntegerField(default=0)
	un_read_remind = models.IntegerField(default=0)
	n_reminds = models.IntegerField(default=0)
	
	n_links = models.IntegerField(default=0)
	n_comments = models.IntegerField(default=0)
	n_discusses = models.IntegerField(default=0)
	
	n_collection = models.IntegerField(default=0)
	n_shares = models.IntegerField(default=0)
	n_support = models.IntegerField(default=0)
	
	
	last_month_half_votes = models.IntegerField(default=0)
	last_month_start_time = models.DateTimeField(null=True, blank=True)
	
	this_month_vote = models.IntegerField(default=0)
	this_month_start_time = models.DateTimeField(null=True, blank=True)
	
	
	def __unicode__(self):
		return self.user.username + ' ' + str(self.honor)
	


class ContentBase(models.Model):
	'''
	'''
	id = models.IntegerField(primary_key=True)
	
	is_visible = models.BooleanField(default=True)
	is_boutique = models.BooleanField(default=False, db_index=True)
	is_can_comment = models.BooleanField(default=True)
	
	n_comments = models.IntegerField(default=0)
	n_collecter = models.IntegerField(default=0)
	n_supporter = models.IntegerField(default=1, db_index=True)
	n_shares = models.IntegerField(default=1)
	
	supporters = generic.GenericRelation(Vote)
	
	shares = generic.GenericRelation(Share)
	
	collecters = generic.GenericRelation(Collect)
	
	class Meta:
		abstract=True
