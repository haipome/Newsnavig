from django.db import models
from django.core.files import File
from django.core.files.storage import default_storage as storage
from os import remove
from time import time
from random import random
from utils import get_avatar
from nng.utils import generate_sha1
from nng.settings import *

class Avatar(models.Model):
	'''
	user's avatars, include small, medium and large avatar. The size are define 
	in setting AVATAR_SMALL, AVATAR_MEDIUM and AVATAR_LARGE.
	
	creat Avatar: 
		a = Avatar()
		a.avatar_save(f) # f can be file or File obj or string of path, this  
		                 # call will automatically call self.save()
	
	change Avatar:
		...get Avatar instance a
		a.avatar_save(f)
	
	delete Avatar:
		a.avatar_delete() # delete the imgs in directory
		a.delete()        # delete the instance in datebase
	'''
	path_prefix = models.CharField(max_length=20, db_index=True)
	is_img_exist = models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.path_prefix
	
	def _get_path(self, t):
		prefix = "%s/%s" % (AVATARS_DIR, self.path_prefix)
		if t == 'small':
			return r"%s_%s.jpg" % (prefix, AVATAR_SMALL_NAME)
		elif t == 'medium':
			return r"%s_%s.jpg" % (prefix, AVATAR_MEDIUM_NAME)
		elif t == 'large':
			return r"%s_%s.jpg" % (prefix, AVATAR_LARGE_NAME)
		elif t == 'origin':
			return r"%s.jpg" % prefix
		else:
			return None
	
	def get_small_url(self):
		if self.is_img_exist:
			return storage.url(self._get_path('small'))
		else:
			return None
	
	def get_medium_url(self):
		if self.is_img_exist:
			return storage.url(self._get_path('medium'))
		else:
			return None
	
	def get_large_url(self):
		if self.is_img_exist:
			return storage.url(self._get_path('large'))
		else:
			return None
	
	def get_origin_url(self):
		if self.is_img_exist:
			return storage.url(self._get_path('origin'))
		else:
			return None
	
	def _avatar_save(self, f, t):
		if t == 'large':
			size = AVATAR_LARGE_SIZE
		elif t == 'medium':
			size = AVATAR_MEDIUM_SIZE
		elif t == 'small':
			size = AVATAR_SMALL_SIZE
		elif t == 'origin':
			size = 0
		else:
			return False
		if size:
			filename = get_avatar(MEDIA_ROOT + self._get_path('origin'), size)
			storage.save(self._get_path(t), File(open(filename)))
			remove(filename)
		else:
			if isinstance(f, File):
				storage.save(self._get_path(t), f)
			elif isinstance(f, file):
				storage.save(self._get_path(t), File(f))
			else:
				storage.save(self._get_path(t), File(open(f)))
	
	def avatar_save(self, upload):
		while True:
			if self.is_img_exist:
				self.avatar_delete()
			# change the url to reload the cache in user browser
			# if self.path_prefix:
			# 	break
			sha_hash = generate_sha1()
			test_prefix = r"%s/%s/%s" % \
			              (sha_hash[0:2], sha_hash[2:4], sha_hash[4:15], )
			test_path = r"%s/%s_%s.jpg" % (AVATARS_DIR, test_prefix, \
			                               str(AVATAR_LARGE_NAME))
			if test_path == storage.get_available_name(test_path):
				self.path_prefix = test_prefix
				self.is_img_exist = True
				break
		self._avatar_save(upload, 'origin')
		self._avatar_save(upload, 'large')
		self._avatar_save(upload, 'medium')
		self._avatar_save(upload, 'small')
		self.is_img_exist = True
		
		self.save()
	
	def _avatar_delete(self, t):
		path = self._get_path(t)
		if path and storage.exists(path):
			storage.delete(path)
		else:
			return False
	
	def avatar_delete(self):
		self._avatar_delete('large')
		self._avatar_delete('medium')
		self._avatar_delete('small')
		self._avatar_delete('origin')
		
		self.is_img_exist = False
		self.save()


def get_tag_avatar():
	try:
		tag_avatar = Avatar.objects.get(pk=TAG_AVATAR_ID)
	except:
		tag_avatar = Avatar(id=TAG_AVATAR_ID)
		tag_avatar.avatar_save(MEDIA_ROOT + TAG_AVATAR_NAME)
	
	return tag_avatar
