#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.hashcompat import sha_constructor
from nng.settings import *
from django.db.models import get_model
from time import time
from random import random

def generate_sha1(string=None):
	if string:
		s = string
	else:
		s = str(time()) + str(random)
	return sha_constructor(s).hexdigest()

