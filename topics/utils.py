#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import Topic, TopicUserShip, TopicDomainShip
from avatars.models import get_tag_avatar
from columns.models import Column
from django.db.models import F
from domains.models import Domain
from columns.utils import create_column
from django.utils.timezone import now

def _creat_topic(name, links=0, discusses=0):
	'''
	'''
	t = Topic.objects.create(name=name,
	                         avatar=get_tag_avatar(),
	                         n_links=links,
	                         n_discusses=discusses)
	create_column(t)
	
	return t
	
def add_link_topic(name, user, url, domain):
	'''
	'''
	try:
		t = Topic.objects.filter(name__iexact=name)[0]
	except:
		t = _creat_topic(name)
	
	if t.topic_links.filter(url__iexact=url).count():
		topic_ship_update(t, user)
		topic_ship_update(t, user=None, domain=domain, is_vote=True)
		return t
	else:
		topic_ship_update(t, user, domain=domain)
		t.n_links += 1
		t.save()
		return t

def add_discuss_topic(name, user):
	'''
	'''
	try:
		t = Topic.objects.filter(name__iexact=name)[0]
	except:
		t = _creat_topic(name)
	
	topic_ship_update(t, user, is_discuss=True)
	t.n_discusses += 1
	t.save()
	
	return t
	

def topic_ship_update_by_name(topic_name, user,
                              domain_name=None,
                              is_discuss=False,
                              is_comment=False):
	'''
	'''
	topic = None
	domain = None
	try:
		topic = Topic.objects.filter(name__iexact=topic_name)[0]
	except:
		return False
	if domain_name:
		try:
			domain = Domain.objects.filter(domain__iexact=domain_name)[0]
		except:
			return False
	
	topic_ship_update(topic, user, domain,
	                  is_discuss, is_comment, is_vote=False)

def _creat_user_ship(user, topic, n_links=0, n_discusses=0):
	TopicUserShip.objects.create(user=user, topic=topic,
	                             n_links=n_links, n_discusses=n_discusses)

def _creat_domain_ship(domain, topic, n_links=0, n_discusses=0):
	TopicDomainShip.objects.create(domain=domain, topic=topic, n_links=n_links)


def topic_ship_update(topic, user,
                      domain = None,
                      is_discuss=False,
                      is_comment=False,
                      is_vote=False):
	
	errorn = 0
	
	if not is_vote:
		if is_discuss:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
		           n_discusses=F('n_discusses') + 1, last_active_time=now()):
				_creat_user_ship(user=user, topic=topic, n_discusses=1)
		elif is_comment:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       n_comments=F('n_comments') + 1):
				errorn += 1
			if domain:
				if not TopicDomainShip.objects.filter(
				       domain=domain, topic=topic).update(
				       n_comments=F('n_comments') + 1):
					errorn += 1
		else:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       n_links=F('n_links') + 1, last_active_time=now()):
				_creat_user_ship(user=user, topic=topic, n_links=1)
			if domain:
				if not TopicDomainShip.objects.filter(
				       domain=domain, topic=topic).update(
				       n_links=F('n_links') + 1):
					_creat_domain_ship(domain=domain, topic=topic, n_links=1)
	else:
		if user:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       votes=F('votes') + 1):
				errorn += 1
		if domain:
			if not TopicDomainShip.objects.filter(domain=domain, topic=topic).update(
			       votes=F('votes') + 1):
				errorn += 1
	
	if not errorn:
		return True
	else:
		return False
	
	
	
