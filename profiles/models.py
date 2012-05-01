from django.db import models
from django.contrib.auth.models import User
from avatars.models import Avatar
from datetime import timedelta
from django.utils.timezone import now
from nng.settings import *
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from columns.models import Column

class UserProfile(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	
	columns = generic.GenericRelation(Column)
	
	username_change_time = models.DateTimeField(blank=True, null=True)
	avatar = models.ForeignKey(Avatar, blank=True, null=True)
	avatar_change_time = models.DateTimeField(blank=True, null=True)
	name = models.CharField(max_length=NAME_MAX_LEN, blank=True)
	name_change_time = models.DateTimeField(blank=True, null=True)
	
	website = models.URLField(blank=True)
	signature = models.CharField(max_length=SIGNATURE_MAX_LEN, blank=True)
	detail = models.TextField(blank=True)
	
	
	def get_name(self):
		if self.name:
			return self.name
		else:
			return self.user.username
	
	def __unicode__(self):
		return self.get_name()
	
	def is_can_change_name(self):
		if not self.name_change_time:
			return True
		can_change_days = timedelta(days=PROFILE_NAME_CHANGE_DAYS)
		can_change_time = self.name_change_time + can_change_days
		
		if now() > can_change_time:
			return True
		else:
			return False
	
	def change_name(self, name):
		if self.is_can_change_name():
			self.name = name
			self.name_change_time = now()
			self.save()
			return True
		else:
			return False
	
	def detail_change(self, data):
		if self.signature != data['signature']:
			self.signature = data['signature']
		if self.detail != data['detail']:
			self.detail = data['detail']
		self.save()
		return True
	
	def get_absolute_url(self):
		return '/people/' + self.user.username + '/'
	
	def get_column(self):
		try:
			return self.columns.all()[0]
		except:
			return None
