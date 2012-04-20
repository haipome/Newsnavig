from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from managers import AccountManager
from nng.utils import generate_sha1
from nng.settings import *

import datetime
	
class UserAccount(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	last_active = models.DateTimeField(blank=True, null=True)
	
	confirm_key = models.CharField(max_length=40, blank=True)
	confirm_key_creat_time = models.DateTimeField(blank=True, null=True)
	is_confirm_key_send = models.BooleanField(default=False)
	
	email_unconfirmed = models.EmailField(blank=True)
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
		if timezone.now() > expiration_date:
			return True
		return False
	
	def send_confirm_email(self):
		'''
		'''
		context = {'user' : self.user,
		           'email' : self.email_unconfirmed,
		           'confirm_key' : self.confirm_key,
		           'effective_days' : ACCOUNT_CONFIRM_DAYS,
		}
		
		if self.user.is_active:
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
				self.is_activkey_send = False
			else:
				self.is_activkey_send = True
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
				self.is_activkey_send = False
			else:
				self.is_activkey_send = True
		self.save()
		if self.is_activkey_send:
			return True
		else:
			return False
	
	def change_email(self, email):
		'''
		'''
		self.email_unconfirmed = email
		self.confirm_key = generate_sha1()
		self.confirm_key_creat_time = timezone.now()
		self.is_confirm_key_send = False
		
		self.send_confirm_email()
