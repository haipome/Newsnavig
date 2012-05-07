from models import Link
from urlparse import urlparse
from domains.utils import add_link_domain
from topics.utils import add_link_topic
from globalvars.utils import get_available_id
from dynamic.models import Dynamic
from nng.settings import *
import googl

def _get_complete_url(url):
	o = urlparse(url)
	if not o[0]:
		url = 'http://' + url
	
	return url

def post_link(user, url, title, topic_names):
	'''
	'''
	url = _get_complete_url(url)
	domain = add_link_domain(url)
	
	if len(url) > URL_MAX_LEN:
		client = googl.Googl("AIzaSyDL2zRCt7DmDZV-1_QQY6HZnterAZ3Kv84")
		try:
			result = client.shorten(url)
		except:
			return False
		else:
			url = result['id']
	
	link = Link(id= get_available_id(), url=url, user=user, title=title)
	
	if domain:
		link.domain = domain
	else:
		return False
	
	for topic_name in topic_names:
		topic = add_link_topic(topic_name, user, url, domain)
		link.topics.add(topic)
	
	link.save()
	
	Dynamic.objects.create(column=domain.get_column(),
	                       way=WAY_LINK_DOMAIN_POST,
	                       content_object=link)
	
	Dynamic.objects.create(column=user.userprofile.get_column(),
	                       way=WAY_LINK_USER_POST,
	                       content_object=link)
	
	return link
	
