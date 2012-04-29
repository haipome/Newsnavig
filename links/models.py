from django.db import models
from django.contrib.auth.models import User
from domains.models import Domain
from topics.models import Topic
from django.contrib.contenttypes import generic
from comments.models import Comment
from votes.models import Vote
from shares.models import Share
from collect.models import Collect


class Link(models.Model):
	'''
	'''
	id = models.IntegerField(primary_key=True)
	
	is_visible = models.BooleanField(default=True)
	is_boutique = models.BooleanField(default=False)
	is_can_comment = models.BooleanField(default=True)
	
	url = models.URLField(max_length=1000)
	title = models.CharField(max_length=210)
	post_time = models.DateTimeField(auto_now_add=True)
	
	post_user = models.ForeignKey(User, related_name="user_links")
	domain = models.ForeignKey(Domain, related_name="domain_links")
	
	topics = models.ManyToManyField(Topic, related_name="topic_links")
	
	n_comments = models.IntegerField(default=0)
	n_collecter = models.IntegerField(default=0)
	n_supporter = models.IntegerField(default=1)
	n_shares = models.IntegerField(default=1)
	
	comments = generic.GenericRelation(Comment)
	
	supporters = generic.GenericRelation(Vote)
	
	shares = generic.GenericRelation(Share)
	
	collecters = generic.GenericRelation(Collect)
	
	
	class Meta:
		ordering = ['-id']
	
	def __unicode__(self):
		return self.title + ' ' +  str(self.n_comments)
	
	
