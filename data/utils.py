from django.contrib.contenttypes.models import ContentType
from models import FollowShip
from django.core.cache import cache
from nng.settings import FOLLOWS_CACHE_AGE

def clear_follows_cache(user):
	'''
	'''
	cache.delete(str(user.id) + 'f')
	cache.delete(str(user.id) + 'bf')

def get_follows(user):
	'''
	'''
	key = str(user.id) + 'f'
	cache_f = cache.get(key)
	if cache_f:
		return cache_f
	
	user_type   = ContentType.objects.get(app_label='profiles', model='userprofile')
	topic_type  = ContentType.objects.get(app_label='topics',   model='topic')
	domain_type = ContentType.objects.get(app_label='domains',  model='domain')
	
	ships = FollowShip.objects.filter(
	          userdata=user.userdata).order_by(
	          '-time').all(
	          ).prefetch_related(
	          'column__content_object__avatar')
	
	follows = []
	follows_user = []
	follows_topic = []
	follows_domain = []
	
	for s in ships:
		c = s.column
		follows.append(c)
		if c.content_type_id == user_type.id:
			follows_user.append((c.content_object, c))
		elif c.content_type_id == topic_type.id:
			follows_topic.append((c.content_object, c))
		elif c.content_type_id == domain_type.id:
			follows_domain.append((c.content_object, c))
		else:
			pass
	
	user_self = user.userprofile.get_column()
	if user_self not in follows:
		follows.append(user.userprofile.get_column())
	
	follows_data = [follows, follows_user, follows_topic, follows_domain, user_self]
	cache.set(key, follows_data, FOLLOWS_CACHE_AGE)
	
	return follows_data


