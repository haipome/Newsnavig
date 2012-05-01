from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from managers import AccountManager
from nng.utils import generate_sha1
from nng.settings import *
from django.utils.timezone import now
from django.dispatch import receiver
from signals import change_email

import datetime
	
class UserAccount(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	last_active = models.DateTimeField(blank=True, null=True)
	
	confirm_key = models.CharField(max_length=CONFIRM_KEY_MAX_LEN, blank=True)
	confirm_key_creat_time = models.DateTimeField(blank=True, null=True)
	is_confirm_key_send = models.BooleanField(default=False)
	
	email_unconfirmed = models.EmailField(blank=True, db_index=True)
	need_change_password = models.BooleanField(default=False)
	
	objects = AccountManager()
	
	def __unicode__(self):
		if self.user.userprofile:
			return self.user.userprofile.__unicode__()
		else:
			return self.user.username
	
	def is_confirm_key_expire(self):
		expiration_days = datetime.timedelta(days=ACCOUNT_CONFIRM_DAYS)
		expiration_date = self.confirm_key_creat_time + expiration_days
		
		if self.confirm_key == ACCOUNT_CONFIRMED:
			return True
		if now() > expiration_date:
			return True
		return False
	
	def send_confirm_email(self):
		'''
		'''
		if self.is_confirm_key_send and self.user.is_active:
			return False
		context = {'user' : self.user,
		           'email' : self.email_unconfirmed,
		           'confirm_key' : self.confirm_key,
		           'effective_days' : ACCOUNT_CONFIRM_DAYS,
		}
		
		if self.user.is_active:
			'''
			subject_old = render_to_string( \
				'accounts/emails/confirm_email_subject_old.txt', \
				context)
			subject_old = ''.join(subject_old.splitlines())
			message_old = render_to_string( \
				'accounts/emails/confirm_email_message_old.txt', \
				context)
				
			try:
				send_mail(subject_old, \
				          message_old, \
				          ACCOUNT_CONFIRM_FROM_EMAIL, \
				          [self.user.email], \
				          fail_silently=False)
			except:
				pass
			'''
			subject_new = render_to_string( \
				'accounts/emails/confirm_email_subject_new.txt', \
				context)
			subject_new = ''.join(subject_new.splitlines())
			message_new = render_to_string( \
				'accounts/emails/confirm_email_message_new.txt', \
				context)
			try:
				send_mail(subject_new, \
				          message_new, \
				          ACCOUNT_CONFIRM_FROM_EMAIL, \
				          [self.email_unconfirmed], \
				          fail_silently=False)
			except:
				self.is_confirm_key_send  = False
			else:
				self.is_confirm_key_send  = True
		else:
			subject = render_to_string( \
				'accounts/emails/activ_email_subject.txt', \
				context)
			subject = ''.join(subject.splitlines())
			message = render_to_string( \
				'accounts/emails/activ_email_message.txt', \
				context)
			try:
				send_mail(subject, \
				          message, \
				          ACCOUNT_CONFIRM_FROM_EMAIL, \
				          [self.email_unconfirmed], \
				          fail_silently=False)
			except:
				self.is_confirm_key_send = False
			else:
				self.is_confirm_key_send = True
		self.save()
		if self.is_confirm_key_send:
			return True
		else:
			return False
	
	def change_email(self, email):
		'''
		'''
		if UserAccount.objects.is_email_regist(email):
			return False
		
		self.email_unconfirmed = email
		self.confirm_key = generate_sha1()
		self.confirm_key_creat_time = now()
		self.is_confirm_key_send = False
		self.save()
		
		self.send_confirm_email()
		
		return True

