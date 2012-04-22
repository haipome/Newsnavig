#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.utils.timezone import now
from nng.settings import REMEMBER_ME_WEEKS

class UserAccountsMiddleware(object):
	def process_request(self, request):
		user = request.user
		if user.is_authenticated():
			user.useraccount.last_active = now()
			user.useraccount.save()
	
	def process_response(self, request, response):
		if not request.session.get_expire_at_browser_close():
			request.session.set_expiry(REMEMBER_ME_WEEKS * 7 * 86400)
		
		return response

