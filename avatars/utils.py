#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib, urllib2, hashlib
from PIL import Image
from tempfile import mktemp
from django.core.files import File

def get_avatar(f, l):
	if isinstance(f, File):
		f = f.file
	try:
		im = Image.open(f)
	except:
		return None
	x, y = im.size
	if x < y:
		s = (y - x) / 2
		box = (0, s, x, s + x)
	else:
		s = (x - y) / 2
		box = (s, 0, y + s, y)
	im = im.crop(box).resize((l, l), Image.ANTIALIAS)
	temp = mktemp() + ".jpg"
	im.convert('RGB').save(temp, "JPEG")
	
	return temp


def get_gravatar(email, size=192, default='404'):
	gravatar_url = "http://www.gravatar.com/avatar/" + \
	               hashlib.md5(email.lower()).hexdigest() + "?"
	gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
	try:
		img_data = urllib2.urlopen(gravatar_url, None, 1).read()
	except:
		return None
	
	temp = mktemp() + ".jpg"
	f = open(temp, 'w+')
	f.write(img_data)
	f.close
	
	return temp


