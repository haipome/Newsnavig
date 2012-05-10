from django.db import models
from django.contrib.auth.models import User
from columns.models import Column
from discusses.models import Discuss

class UserData(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	
	n_follows = models.IntegerField(default=0)
	follows = models.ManyToManyField(Column,
	                                 through="FollowShip",
	                                 related_name="column_followers")
	
	discusses = models.ManyToManyField(Discuss, related_name="discuss_users")
	
	n_follows_user   = models.IntegerField(default=0)
	n_follows_topic  = models.IntegerField(default=0)
	n_follows_domain = models.IntegerField(default=0)
	
	honor = models.IntegerField(default=1)
	
	un_read_messages = models.IntegerField(default=0)
	un_read_remind = models.IntegerField(default=0)
	n_reminds = models.IntegerField(default=0)
	
	n_links = models.IntegerField(default=0)
	n_comments = models.IntegerField(default=0)
	n_discusses = models.IntegerField(default=0)
	n_collections = models.IntegerField(default=0)
	n_shares = models.IntegerField(default=0)
	n_supports = models.IntegerField(default=0)
	
	
	last_month_half_votes = models.IntegerField(default=0)
	last_month_start_time = models.DateTimeField(null=True, blank=True)
	
	this_month_vote = models.IntegerField(default=0, db_index=True)
	this_month_start_time = models.DateTimeField(null=True, blank=True)
	
	
	def __unicode__(self):
		return self.user.username + ' ' + str(self.honor)
	


class FollowShip(models.Model):
	'''
	'''
	userdata = models.ForeignKey(UserData)
	column   = models.ForeignKey(Column)
	
	time = models.DateTimeField(auto_now_add=True, db_index=True)
	
	class Meta:
		ordering = ['-time']
	

