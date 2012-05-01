from django.db import models
from django.contrib.auth.models import User
from domains.models import Domain
from topics.models import Topic
from django.contrib.contenttypes import generic
from comments.models import Comment
from votes.models import Vote
from shares.models import Share
from collect.models import Collect
from nng.settings import TITLE_MAX_LEN, URL_MAX_LEN
from data.models import ContentBase


class Link(ContentBase):
	'''
	'''
	url = models.URLField(max_length=URL_MAX_LEN, db_index=True)
	title = models.CharField(max_length=TITLE_MAX_LEN)
	post_time = models.DateTimeField(auto_now_add=True)
	post_user = models.ForeignKey(User, related_name="user_links")
	
	domain = models.ForeignKey(Domain, related_name="domain_links")
	topics = models.ManyToManyField(Topic, related_name="topic_links")
	
	comments = generic.GenericRelation(Comment)
	
	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.title + ' ' +  str(self.n_comments)
	
	
