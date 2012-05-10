from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic
from django.contrib.contenttypes import generic
from comments.models import Comment
from votes.models import Vote
from shares.models import Share
from collect.models import Collect
from nng.settings import TITLE_MAX_LEN
from globalvars.models import ContentBase
from domains.models import Domain
from columns.models import Column

class Discuss(ContentBase):
	'''
	'''
	user = models.ForeignKey(User, related_name="user_discusses")
	
	title = models.CharField(max_length=TITLE_MAX_LEN)
	detail = models.TextField(blank=True)
	
	domain = models.ForeignKey(Domain, related_name="domain_discusses", null=True, blank="true") # not user
	topics = models.ManyToManyField(Topic, related_name="topic_discusses")
	
	comments = generic.GenericRelation(Comment)
	
	last_active_time = models.DateTimeField(db_index=True)
	last_active_user = models.ForeignKey(User, related_name="user_last_discuss")
	
	class Meta:
		ordering = ["-id"]
	
	def __unicode__(self):
		return self.title + ' ' + str(self.n_comment)
	
	def get_absolute_url(self):
		return '/%s/%s/' % ('discuss', str(self.id))
	

class DiscussIndex(models.Model):
	'''
	'''
	is_visible = models.BooleanField(default=True, db_index=True)
	
	column = models.ForeignKey(Column, related_name="column_discuss_indexs")
	way = models.CharField(max_length=1)
	
	discuss = models.ForeignKey(Discuss, related_name="discuss_indexs")
	
	last_active_time = models.DateTimeField(db_index=True)
	last_active_user = models.ForeignKey(User,
	                                     related_name="user_discuss_indexs",
	                                     null=True)
	

