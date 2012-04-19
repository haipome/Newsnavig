#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.hashcompat import sha_constructor
from nng.settings import *
from django.db.models import get_model

def generate_sha1(string):
	return sha_constructor(str(string)).hexdigest()

def get_profile_model():
	"""
	Return the model class for the currently-active user profile
	model, as defined by the ``AUTH_PROFILE_MODULE`` setting.

	:return: The model that is used as profile.
	
	"""
	if not AUTH_PROFILE_MODULE:
		raise SiteProfileNotAvailable

	profile_mod = get_model(*AUTH_PROFILE_MODULE.split('.'))
	if profile_mod is None:
		raise SiteProfileNotAvailable
	return profile_mod
