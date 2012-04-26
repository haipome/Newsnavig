from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
	'''
	'''
	user = models.OneToOneField(User)
	un_read_messages = models.IntegerField(default=0)
