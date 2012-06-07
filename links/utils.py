from models import Link
from urlparse import urlparse
from domains.utils import add_link_domain
from topics.utils import add_link_topic
from globalvars.utils import get_available_id
from dynamic.models import Dynamic
from nng.settings import *
from data.models import UserData
from django.db.models import F
import googl
from topics.utils import del_link_topic
from domains.utils import del_link_domain

def post_link(user, url, title, topic_names):
	'''
	'''
	domain, domain_post = add_link_domain(url)
	
	link = Link(id= get_available_id(), url=url, user=user, title=title)
	
	if domain:
		link.domain = domain
	else:
		return False
	
	if len(url) > URL_MAX_LEN:
		client = googl.Googl("AIzaSyDL2zRCt7DmDZV-1_QQY6HZnterAZ3Kv84")
		try:
			result = client.shorten(url)
		except:
			return False
		else:
			url = result['id']
			link.url = url
	link.save()
	
	for topic_name in topic_names:
		topic = add_link_topic(topic_name, user, url, domain)
		link.topics.add(topic)
		
		if not FILTER:
			if topic.topic_links.filter(url__iexact=url).count() == 1:
				Dynamic.objects.create(column=topic.get_column(),
				                       way=WAY_LINK_TOPIC_POST,
				                       content_object=link)
	
	if not domain_post:
		Dynamic.objects.create(column=domain.get_column(),
		                       way=WAY_LINK_DOMAIN_POST,
		                       content_object=link)
	
	
	Dynamic.objects.create(column=user.userprofile.get_column(),
	                       way=WAY_LINK_USER_POST,
	                       content_object=link)
	
	UserData.objects.filter(user=user).update(n_links=F('n_links') + 1)
	
	return link
	

def del_link(l):
	if not isinstance(l, Link):
		return False
	
	data = l.user.userdata
	data.n_links -= 1
	data.save()
	
	for t in l.topics.all():
		del_link_topic(l, t)
	
	del_link_domain(l)
	
	return True
