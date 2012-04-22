from django.db import models
from django.contrib.auth.models import User
from avatars.models import Avatar
from datetime import timedelta
from django.utils.timezone import now
from nng.settings import *

class UserProfile(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	username_change_time = models.DateTimeField(blank=True, null=True)
	avatar = models.ForeignKey(Avatar)
	avatar_change_time = models.DateTimeField(blank=True, null=True)
	name = models.CharField(max_length=30, blank=True)
	name_change_time = models.DateTimeField(blank=True, null=True)
	
	website = models.URLField(max_length=200, blank=True)
	signature = models.CharField(max_length=210, blank=True)
	detail = models.TextField(max_length=3000, blank=True)
	
	
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
