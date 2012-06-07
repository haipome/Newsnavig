#!/usr/bin/python
# -*- coding: utf-8 -*-

from models import Topic, TopicUserShip, TopicDomainShip
from avatars.models import get_tag_avatar
from columns.models import Column
from django.db.models import F
from domains.models import Domain
from columns.utils import create_column
from django.utils.timezone import now
from links.models import Link
from discusses.models import Discuss
from discusses.models import DiscussIndex
from dynamic.models import Dynamic
from django.core.cache import cache
from nng.settings import HOT_TOPICS_CACHE_AGE
from topics.models import Topic

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

def del_link_topic(l, t):
	'''
	'''
	if not isinstance(l, Link):
		return False
	
	Dynamic.objects.filter(column=t.get_column()
	                ).filter(object_id=l.id).update(
	                is_visible=False)
	
	if t.topic_links.filter(url__iexact=l.url).count() == 1:
		t.n_links -= 1
	
	if l.is_boutique:
		t.n_links_boutiques -= 1
	
	topic_ship_update(t, l.user, domain=l.domain, num=-1)
	t.save()
	

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
	

def del_discuss_topic(d, t):
	'''
	'''
	if not isinstance(d, Discuss):
		return False
	column = t.get_column()
	
	Dynamic.objects.filter(column=column
	                ).filter(object_id=d.id).update(
	                is_visible=False)
	DiscussIndex.objects.filter(column=column
	                     ).filter(discuss_id=d.id).update(
	                     is_visible=False)
	
	t.n_discusses -= 1
	if d.is_boutique:
		t.n_links_boutiques -= 1
	topic_ship_update(t, d.user, is_discuss=True, num=-1)
	t.save()
	

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
                      is_vote=False,
                      num = 1):
	
	errorn = 0
	
	if not is_vote:
		if is_discuss:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
		           n_discusses=F('n_discusses') + num, last_active_time=now()):
				_creat_user_ship(user=user, topic=topic, n_discusses=1)
		elif is_comment:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       n_comments=F('n_comments') + num):
				errorn += 1
			if domain:
				if not TopicDomainShip.objects.filter(
				       domain=domain, topic=topic).update(
				       n_comments=F('n_comments') + num):
					errorn += 1
		else:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       n_links=F('n_links') + 1, last_active_time=now()):
				_creat_user_ship(user=user, topic=topic, n_links=1)
			if domain:
				if not TopicDomainShip.objects.filter(
				       domain=domain, topic=topic).update(
				       n_links=F('n_links') + num):
					_creat_domain_ship(domain=domain, topic=topic, n_links=1)
	else:
		if user:
			if not TopicUserShip.objects.filter(user=user, topic=topic).update(
			       votes=F('votes') + num):
				errorn += 1
		if domain:
			if not TopicDomainShip.objects.filter(domain=domain, topic=topic).update(
			       votes=F('votes') + 1):
				errorn += 1
	
	if not errorn:
		return True
	else:
		return False
	


def get_hot_topic(n):
	
	key = 'hot_topics%s' % str(n)
	
	hot_topics = cache.get(key)
	if hot_topics:
		return hot_topics
	else:
		topics = Topic.objects.order_by('-n_links')[:n]
		cache.set(key, topics, HOT_TOPICS_CACHE_AGE)
		return topics
	
