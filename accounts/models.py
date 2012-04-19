from django.db import models
from django.contrib.auth.models import User
from avatars.models import Avatar
from managers import AccountManager

import datetime

class UserProfile(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	avatar = models.ForeignKey(Avatar)
	name = models.CharField(max_length=30, blank=True, unique=True)
	website = models.URLField(blank=True)
	
	signature = models.CharField(max_length=210, blank=True)
	detail = models.TextField(max_length=3000, blank=True)
	
	def __unicode__(self):
		if name:
			return self.name
		else:
			return self.user.username
	
class UserAccount(models.Model):
	'''
	'''
	user = models.OneToOneField(UserProfile)
	last_active = models.DateTimeField(blank=True, null=True)
	
	activkey = models.CharField(max_length=40, blank=True)
	activkey_creat_time = models.DateTimeField(blank=True, null=True)
	is_activkey_send = models.BooleanField(default=False)
	
	email_unconfirmed = models.EmailField(blank=True)
	email_confirmkey = models.CharField(max_length=40, blank=True)
	email_confirmkey_creat_time = models.DateTimeField(blank=True, null=True)
	is_confirmkey_send = models.BooleanField(default=False)
	
	objects = AccountManager()
	
	def __unicode__(self):
		return self.user.__unicode__()
	
	def is_activkey_expire(self):
		expiration_days = datetime.timedelta(days=ACCOUNT_ACTIV_DAYS)
		expiration_date = self.activkey_creat_time + expiration_days
		if self.activkey == ACCOUNT_ACTIVATED:
			return True
		if timezone.now() > expiration_date:
			return True
		return False
	
	
