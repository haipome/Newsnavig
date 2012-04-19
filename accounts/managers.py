#!/usr/bin/python
# -*- coding: utf-8 -*-

from nng.settings import *
from django.db import models
from django.contrib.auth.models import User, UserManager, Permission
from django.utils import timezone
from nng.utils import generate_sha1, get_profile_model
from time import time
from random import random

import re
SHA1_RE = re.compile('^[a-f0-9]{40}$')

class AccountManager(UserManager):
	'''
	'''
	def create_user(self, username, email, password):
		'''
		'''
		new_user = User.objects.create_user(username, email, password)
		new_user.is_active = False
		new_user.save()
		
		activkey = generate_sha1(str(time) + str(random))
		account = self.creat(user=new_user, activkey=activkey, \
		           activkey_creat_time = timezone.now())
		account.last_active = timezone.now()
		account.save()
		
		profile_model = get_profile_model()
		try:
			profile = new_user.get_profile()
		except profile_model.DoesNotExist:
			profile = profile_model(user=new_user)
		
		anonymous = User.objects.get(pk=ANONYMOUS_ID)
		profile.avatar = anonymous.userprofile.avatar
		profile.save()
		
		account.send_activ_mail()
		
		return new_user
	
	def activ_user(self, username, activkey):
		'''
		'''
		if SHA1_RE.search(activation_key):
			try:
				account = self.get(user__username=username, \
				                   activkey=activkey)
			except self.model.DoesNotExist:
				return False
			if not account.is_activkey_expire():
				account.activkey = ACCOUNT_ACTIVATED
				user = account.user
				user.is_active = True
				user.save()
				account.last_active = timezone.now()
				account.save()
				'''
				can add other action here.
				'''
				return user
		
		return False
	
	def confirm_email(self, username, confirmkey):
		'''
		'''
		if SHA1_RE.search(activation_key):
			try:
				account = self.get(user__username=username, \
				                   email_confirmkey = confirmkey)
			except self.model.DoesNotExist:
				return False
			else:
				user = account.user
				user.email = account.email_unconfirmed
				user.save()
				account.email_unconfirmed = ''
				account.email_confirmkey = ''
				account.save()
				
				return user
		
		return False
		
	def delete_expired_users(self):
		'''
		'''
		deleted_users = []
		for user in User.objects.filter(is_staff=False, is_active=False):
			if user.useraccount.is_activkey_expire():
				deleted_users.append(user)
				user.delete()
		return deleted_users
	
