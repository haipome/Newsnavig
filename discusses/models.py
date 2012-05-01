from django.db import models
from django.contrib.auth.models import User
from topics.models import Topic
from django.contrib.contenttypes import generic
from comments.models import Comment
from votes.models import Vote
from shares.models import Share
from collect.models import Collect
from nng.settings import TITLE_MAX_LEN
from data.models import ContentBase

class Discuss(ContentBase):
	'''
	'''
	title = models.CharField(max_length=TITLE_MAX_LEN)
	detail = models.TextField(blank=True)
	
	start_user = models.ForeignKey(User)
	start_time = models.DateTimeField(auto_now_add=True)
	last_active_time = models.DateTimeField(blank=True, null=True)
	
	topics = models.ManyToManyField(Topic, related_name="topic_discuss")
	
	comments = generic.GenericRelation(Comment)
	
	class Meta:
		ordering = ["-last_active_time"]
	
	def __unicode__(self):
		return self.title + ' ' + str(self.n_comments)
	
	
	
	