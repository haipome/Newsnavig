#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import UserProfile
from nng.utils import generate_sha1
from nng.settings import *
from avatars.models import Avatar
from signals import create_user_done
from django.dispatch import receiver
from avatars.utils import get_gravatar
from avatars.models import Avatar
from os import remove
from django.utils.timezone import now
from data.models import UserData
from columns.utils import create_column

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
		                 password=ANONYMOUS_PASSWORD) # this password will 
		                                              # never be used!
		anonymous.save()
		avatar = Avatar()
		avatar.avatar_save(MEDIA_ROOT + ANONYMOUS_USERNAME + '.jpg')
		
		profile = UserProfile(user=anonymous)
		profile.avatar=avatar
		profile.name = ANONYMOUS_NAME
		profile.save()
		
		# there while add some other thing
		
		return anonymous
	
	def create_user(self, username, email, password):
		'''
		'''
		try:
			user = User.objects.filter(username__iexact=username)
		except:
			user = None
		if user:
			return False
			
		try:
			user = User.objects.filter(email__iexact=email)
		except:
			user = None
		if user:
			return False
		
		try:
			user = UserProfile.objects.filter(email_unconfirmed__iexact = email)
		except:
			user = None
		if user:
			return False
		
		new_user = User.objects.create_user(username=username, password=password)
		new_user.is_active = False
		new_user.save()
		
		confirm_key = generate_sha1()
		account = self.create(user=new_user, \
		          confirm_key=confirm_key, \
		          confirm_key_creat_time = now(), \
		          email_unconfirmed = email, \
		          last_active = now())
		account.send_confirm_email()
		
		profile = UserProfile(user=new_user)
		try:
			anonymous = User.objects.get(pk=ANONYMOUS_ID)
		except:
			anonymous = self.create_anonymous()
		profile.avatar = anonymous.userprofile.avatar
		profile.name = username
		profile.save()
		
		# print 'send create_user_done signal'
		# create_user_done.send(sender='UserAccount', user=new_user)
		filename = get_gravatar(account.email_unconfirmed)
		if filename:
			avatar = Avatar()
			avatar.avatar_save(filename)
			remove(filename)
			profile.avatar = avatar
			profile.save()
		
		return new_user
	
	def confirm_email(self, username, confirm_key):
		'''
		'''
		if SHA1_RE.search(confirm_key):
			try:
				account = self.get(user__username=username)
			except self.model.DoesNotExist:
				return False
			if not account.is_confirm_key_expire():
				if account.confirm_key == ACCOUNT_CONFIRMED:
					return False
				if account.confirm_key != confirm_key:
					return False
				account.confirm_key = ACCOUNT_CONFIRMED
				user = account.user
				if account.email_unconfirmed:
					if User.objects.filter(email__iexact=account.email_unconfirmed):
						return False
					user.email = account.email_unconfirmed
					account.email_unconfirmed = ''
				if not user.is_active:
					user.is_active = True
					
					# create user data
					create_column(user.userprofile)
					UserData.objects.create(user=user)
					'''
					will do some other thing here
					'''
				user.save()
				account.last_active = now()
				account.save()
				
				return user
			else:
				account.email_unconfirmed = ''
				account.save()
				
				return False
		
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
	
	def is_email_regist(self, email):
		'''
		'''
		if self.filter(email_unconfirmed__iexact=email) or \
		   User.objects.filter(email__iexact=email):
			return True
		else:
			return False
