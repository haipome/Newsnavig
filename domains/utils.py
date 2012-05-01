from domains.models import Domain
from columns.models import Column
from avatars.models import get_tag_avatar
from django.db.models import F
from urlparse import urlparse
from links.models import Link
from columns.utils import create_column

def _create_domain(domain):
	'''
	'''
	d = Domain.objects.create(domain=domain,
	                          avatar=get_tag_avatar())
	create_column(d)
	
	return d

def get_domain(url):
	'''
	'''
	try:
		d = urlparse(url)[1]
	except:
		return False
	
	items = d.split('.')
	if items[0] == 'www':
		return '.'.join(items[1:])
	else:
		return d


def add_link_domain(url):
	'''
	'''
	name = get_domain(url)
	if not name:
		return False
	try:
		d = Domain.objects.filter(domain__iexact=name)[0]
	except:
		d= _create_domain(name)
	
	if d.domain_links.filter(url__iexact=url).count():
		return d
	else:
		d.n_links += 1
		d.save()
		return d
	
