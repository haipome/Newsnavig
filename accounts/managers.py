#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from profiles.models import UserProfile
from nng.utils import generate_sha1
from nng.settings import *
from avatars.models import Avatar
from signals import create_user_done
from django.dispatch import receiver
from avatars.utils import get_gravatar
from avatars.models import Avatar
from os import remove

import re
SHA1_RE = re.compile('^[a-f0-9]{40}$')

class AccountManager(UserManager):
	'''
	'''
	def create_anonymous(self):
		'''
		'''
		anonymous = User(id=ANONYMOUS_ID, \
		                 username=ANONYMOUS_USERNAME, \
		                 password=ANONYMOUS_PASSWORD)
		anonymous.save()
		avatar = Avatar()
		avatar.avatar_save(MEDIA_ROOT + ANONYMOUS_USERNAME + '.jpg')
	
		profile = UserProfile(user=anonymous)
		profile.avatar=avatar
		profile.name = ANONYMOUS_NAME
		profile.save()
	
		return anonymous
	
	def create_user(self, username, email, password):
		'''
		'''
		new_user = User(username=username, password=password)
		new_user.is_active = False
		new_user.save()
		
		confirm_key = generate_sha1()
		account = self.create(user=new_user, \
		          confirm_key=confirm_key, \
		          confirm_key_creat_time = timezone.now(), \
		          email_unconfirmed = email, \
		          last_active = timezone.now())
		# account.send_confirm_email()
		
		try:
			anonymous = User.objects.get(pk=ANONYMOUS_ID)
		except:
			anonymous = self.create_anonymous()
		profile = UserProfile(user=new_user, \
		          avatar = anonymous.userprofile.avatar)
		profile.save()
		
		# print 'send create_user_done signal'
		create_user_done.send(sender='UserAccount', user=new_user)
		
		return new_user
	
	def confirm_email(self, username, confirm_key):
		'''
		'''
		if SHA1_RE.search(confirm_key):
			try:
				account = self.get(user__username=username, \
				                   confirm_key=confirm_key)
			except self.model.DoesNotExist:
				return False
			if not account.is_confirm_key_expire():
				account.activkey = ACCOUNT_CONFIRMED
				user = account.user
				if account.email_unconfirmed:
					user.email = account.email_unconfirmed
					account.email_unconfirmed = ''
				if not user.is_active:
					user.is_active = True
					'''
					will do some other thing here
					'''
				user.save()
				account.last_active = timezone.now()
				account.save()
				
				return user
		
		return False
	
	def delete_expired_users(self):
		'''
		'''
		deleted_users = []
		for user in User.objects.filter(is_staff=False, is_active=False):
			if user.useraccount.is_confirm_key_expire():
				deleted_users.append(user)
				user.delete() # while also delete the OneToOneField
		return deleted_users

@receiver(create_user_done, \
          sender = 'UserAccount', \
          dispatch_uid="get gravatar and send conirm email")
def create_user_done_handler(sender, user, **kwargs):
	'''
	'''
	# print 'works'
	filename = get_gravatar(user.useraccount.email_unconfirmed)
	if filename:
		avatar = Avatar()
		avatar.avatar_save(filename)
		remove(filename)
		user.userprofile.avatar = avatar
		user.userprofile.save()
	else:
		try:
			anonymous = User.objects.get(pk=ANONYMOUS_ID)
		except:
			anonymous = user.useraccount.objects.create_anonymous()
		user.userprofile.avata = anonymous.userprfile.avatar
	
	user.useraccount.send_confirm_email()
