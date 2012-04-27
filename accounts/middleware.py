#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.timezone import now
from nng.settings import REMEMBER_ME_WEEKS
from datetime import datetime

class UserAccountsMiddleware(object):
	def process_response(self, request, response):
		try:
			user = request.user
		except:
			return response
		if user.is_authenticated():
			try:
				if not request.session.get_expire_at_browser_close():
					if user.useraccount.last_active.date() != \
					   datetime.utcnow().date():
						request.session.set_expiry(REMEMBER_ME_WEEKS * 7 * 86400)
				user.useraccount.last_active = now()
				user.useraccount.save()
			except:
				pass
		return response

